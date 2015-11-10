package quiklyrics

import (
	"encoding/json"
	"net/http"
)

type SuggestResponse struct {
	Suggestions []string `json:"suggestions"`
}

type SearchResponse struct {
	Lyrics Lyrics `json:"lyrics"`
}

func suggestFake(query string) []string {
	return []string{"Hey ya", "Boo yeah"}
}

func searchFake(query string) Lyrics {
	return Lyrics{"testing\ntesting again", "Jack Title"}
}

func SuggestServer(w http.ResponseWriter, r *http.Request) {
	UpdateFetcher(r)
	b, e := json.Marshal(SuggestResponse{Suggest(r.URL.Query().Get("lyrics"))})
	if e != nil {
		panic(e)
	}
	w.Write(b)
}

func SearchServer(w http.ResponseWriter, r *http.Request) {
	UpdateFetcher(r)
	query := r.URL.Query().Get("lyrics")
	lyrics, e := GetLyricsForQuery(query)
	if e != nil {
		panic(e)
	}
	b, e := json.Marshal(SearchResponse{lyrics})
	if e != nil {
		panic(e)
	}
	w.Write(b)
}
