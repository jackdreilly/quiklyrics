package quiklyrics

import (
	"fmt"
	"testing"
)

// func TestLyrics(t *testing.T) {
// 	fmt.Println(LyricsFreak("http://www.lyricsfreak.com/r/r+kelly/i+believe+i+can+fly_20113006.html"))
// }

func TestMetro(t *testing.T) {
	// fmt.Println(GetLyricsForQuery("and so we've come to the end of the road"))

	// fmt.Println(AzLyrics("http://www.azlyrics.com/lyrics/boyziimen/endoftheroad.html"))
	// c, _, _ := aetest.NewContext()
	// client := urlfetch.Client(c)
	// fmt.Println(client)
	// url := "http://www.azlyrics.com/lyrics/boyziimen/endoftheroad.html"
	// req, _ := http.NewRequest("GET", url, nil)
	// req.Header.Add("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0-AppEngine")
	// // f, e := client.Do(req)
	// f, e := http.DefaultClient.Do(req)
	// fmt.Println(f)
	// if e != nil {
	// 	fmt.Println(e)
	// }
	// fmt.Println("hi")
	// fmt.Println(f)
	// l, _ := MetroLyrics("http://www.metrolyrics.com/give-me-one-reason-lyrics-tracy-chapman.html")
	// fmt.Println(l.Title)
	// fmt.Println(GetLyricsForQuery("uptown funk lyricsfreak"))
	// fmt.Println(AzLyrics("http://www.azlyrics.com/lyrics/dawes/alittlebitofeverything.html"))
	fmt.Println(GetLyricsForQuery("all your favorite bands dawes"))
}
