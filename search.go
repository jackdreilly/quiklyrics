package quiklyrics

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"net/url"

	"google.golang.org/api/customsearch/v1"
)

const (
	key           = "AIzaSyBInAHol7AwVGNV8mmUf8VnRgY6H-s8Rn4"
	searchBaseURL = "https://www.googleapis.com/customsearch/v1?cx=001283733761018543620%3Aujg1bejtz_y&key=" + key + "&q="
)

type Result struct {
	resultUrl string
	title     string
}

func GoogleSearch(query string) []Result {
	requestURL := searchBaseURL + url.QueryEscape("lyrics "+query)
	res, err := CurrentFetcher.Get(requestURL)
	if err != nil {
		log.Println(requestURL)
		log.Println(query)
		panic(err)
	}

	defer res.Body.Close()
	body, err := ioutil.ReadAll(res.Body)
	if err != nil {
		panic(err)
	}

	var data customsearch.Search
	err = json.Unmarshal(body, &data)
	if err != nil {
		panic(err)
	}
	var results = make([]Result, 0)
	for _, item := range data.Items {
		results = append(results, Result{item.Link, item.Title})
	}
	return results
}

func (r *Result) URL() string {
	return r.resultUrl
}
