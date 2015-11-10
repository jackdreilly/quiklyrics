package quiklyrics

import (
	"net/url"
	"strings"

	"github.com/PuerkitoBio/goquery"
)

const (
	baseURL = "http://suggestqueries.google.com/complete/search?output=toolbar&hl=en&q="
)

// url gives suggest url for query string
func suggestUrl(query string) string {
	lyricsQuery := "lyrics " + query
	return baseURL + url.QueryEscape(lyricsQuery)
}

// Suggest uses google suggest to return suggestions for current query
func Suggest(query string) []string {
	doc, err := CurrentFetcher.Fetch(suggestUrl(query))
	if err != nil {
		panic(err)
	}
	var results = make([]string, 0)
	doc.Find("suggestion").Each(func(i int, s *goquery.Selection) {
		data := s.AttrOr("data", "")
		if len(data) > 0 {
			results = append(results, strings.Replace(data, "lyrics ", "", 1))
		}
	})
	return results
}
