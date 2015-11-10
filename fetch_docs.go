package quiklyrics

import (
	"net/http"

	"github.com/PuerkitoBio/goquery"
	"google.golang.org/appengine"
	"google.golang.org/appengine/urlfetch"
)

type DocFetcher interface {
	Fetch(urlString string) (*goquery.Document, error)
	Get(urlString string) (*http.Response, error)
}

type standardFetcher int

func (s standardFetcher) Fetch(urlString string) (*goquery.Document, error) {
	return goquery.NewDocument(urlString)
}

func (s standardFetcher) Get(urlString string) (*http.Response, error) {
	return http.Get(urlString)
}

const (
	Fetcher = standardFetcher(1)
)

var (
	AppEngine = false
)

func UpdateFetcher(r *http.Request) {
	if AppEngine {
		CurrentFetcher = NewAppEngineFetcher(r)
	}
}

var (
	CurrentFetcher DocFetcher = Fetcher
)

type appEngineFetcher struct {
	request *http.Request
}

func NewAppEngineFetcher(r *http.Request) DocFetcher {
	return appEngineFetcher{r}
}

func (a appEngineFetcher) Fetch(urlString string) (*goquery.Document, error) {
	resp, _ := a.Get(urlString)
	return goquery.NewDocumentFromResponse(resp)
}

func (a appEngineFetcher) Get(urlString string) (*http.Response, error) {
	c := appengine.NewContext(a.request)
	client := urlfetch.Client(c)
	return client.Get(urlString)
}
