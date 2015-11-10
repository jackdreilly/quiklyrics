package quiklyrics

import (
	"bytes"
	"errors"
	"log"
	"strings"

	"github.com/PuerkitoBio/goquery"
)

type Lyrics struct {
	Lyrics string
	Title  string
}

func LyricsFreak(link string) (Lyrics, error) {
	doc, err := CurrentFetcher.Fetch(link)
	if err != nil {
		log.Println("failed for " + link)
		return Lyrics{}, errors.New("no match")
	}
	find := doc.Find("#content_h")
	if find.Length() < 1 {
		log.Println("failed for " + link)
		return Lyrics{}, errors.New("no match")
	}
	var buffer bytes.Buffer
	var child = find.Get(0).FirstChild
	for child != nil {
		for child.Data == "br" {
			child = child.NextSibling
		}
		buffer.WriteString(child.Data)
		buffer.WriteString("\n")
		child = child.NextSibling
	}
	titleFind := doc.Find("title")
	if titleFind.Length() < 1 {
		return Lyrics{}, errors.New("no title")
	}
	title := strings.Replace(strings.Replace(titleFind.Get(0).FirstChild.Data, " | LyricsFreak", "", 1), " Lyrics", "", 1)
	return Lyrics{buffer.String(), title}, nil
}

func DirectLyrics(link string) (Lyrics, error) {
	doc, err := CurrentFetcher.Fetch(link)
	if err != nil {
		log.Println("failed for " + link)
		return Lyrics{}, errors.New("no match")
	}
	find := doc.Find(".lyrics p")
	if find.Length() < 1 {
		log.Println("failed for " + link)
		return Lyrics{}, errors.New("no match")
	}
	var buffer bytes.Buffer
	var child = find.Get(0).FirstChild
	for child != nil {
		for child.Data == "br" {
			child = child.NextSibling
		}
		buffer.WriteString(child.Data)
		child = child.NextSibling
	}
	titleFind := doc.Find("title")
	if titleFind.Length() < 1 {
		return Lyrics{}, errors.New("no title")
	}
	title := strings.Replace(titleFind.Get(0).FirstChild.Data, " LYRICS", "", 1)
	return Lyrics{buffer.String(), title}, nil
}

func AzLyrics(link string) (Lyrics, error) {
	doc, err := CurrentFetcher.Fetch(link)
	if err != nil {
		log.Println("no doc for " + link)
		return Lyrics{}, errors.New("no doc fetch")
	}
	find := doc.Find(".main-page .row .col-xs-12.col-lg-8.text-center div:not([class]):not([data-id])")
	if find.Length() < 1 {
		log.Println("no lyrics for " + link)
		return Lyrics{}, errors.New("no lyrics found")
	}
	var buffer bytes.Buffer
	var child = find.Get(0).FirstChild.NextSibling.NextSibling
	for child != nil {
		for child.Data == "br" {
			child = child.NextSibling
		}
		buffer.WriteString(child.Data)
		child = child.NextSibling
	}
	titleFind := doc.Find("title")
	if titleFind.Length() < 1 {
		log.Println("no lyrics for " + link)
		return Lyrics{}, errors.New("no title")
	}
	title := strings.Replace(titleFind.Get(0).FirstChild.Data, " LYRICS", "", 1)
	return Lyrics{buffer.String(), title}, nil
}

func MetroLyrics(link string) (Lyrics, error) {
	doc, err := CurrentFetcher.Fetch(link)
	if err != nil {
		log.Println("failed for " + link)
		return Lyrics{}, errors.New("no match")
	}
	titleFind := doc.Find("title")
	if titleFind.Length() < 1 {
		return Lyrics{}, errors.New("no title")
	}
	title := strings.Replace(strings.Replace(titleFind.Get(0).FirstChild.Data, " | MetroLyrics", "", 1), " Lyrics", "", 1)
	find := doc.Find(".verse")
	if find.Length() < 1 {
		return Lyrics{}, errors.New("no match")
	}
	var buffer bytes.Buffer
	find.Each(func(i int, s *goquery.Selection) {
		var child = s.Get(0).FirstChild
		for child != nil {
			for child.Data == "br" {
				child = child.NextSibling
			}
			buffer.WriteString(child.Data)
			child = child.NextSibling
		}
		buffer.WriteString("\n\n")
	})

	return Lyrics{buffer.String(), title}, nil
}

func GetLyrics(searchResults []Result) (Lyrics, error) {
	for _, result := range searchResults {
		log.Println(result)
		if strings.Contains(result.URL(), "lyricsfreak.com") {
			lyrics, err := LyricsFreak(result.URL())
			if err == nil {
				return lyrics, nil
			}
		} else if strings.Contains(result.URL(), "metrolyrics.com") {
			lyrics, err := MetroLyrics(result.URL())
			if err == nil {
				return lyrics, nil
			}
		} else if strings.Contains(result.URL(), "directlyrics.com") {
			lyrics, err := DirectLyrics(result.URL())
			if err == nil {
				return lyrics, nil
			}
		} else if strings.Contains(result.URL(), "azlyrics.com") {
			lyrics, err := AzLyrics(result.URL())
			if err == nil {
				return lyrics, nil
			}
		}
	}
	return Lyrics{}, errors.New("No matches")
}

func GetLyricsForQuery(query string) (Lyrics, error) {
	return GetLyrics(GoogleSearch(query))
}
