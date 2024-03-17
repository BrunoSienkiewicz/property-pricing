package fetch

import (
	"fmt"
	"net/http"
)

type Fetcher struct {
	userAgent  string
	urls       []string
	results    map[string]string
	failedUrls []string
	chFailed   chan string
	chDone     chan bool
}

type FetcherInterface interface {
	fetchUrl(url string)
	processResults()

	Fetch()
	GetResults() map[string]string
	GetFailedUrls() []string
}

func NewFetcher(userAgent string, urls []string) *Fetcher {
	return &Fetcher{
		userAgent: userAgent,
		urls:      urls,
		chFailed:  make(chan string),
		chDone:    make(chan bool),
	}
}

func (f *Fetcher) fetchUrl(url string) {
	client := &http.Client{}
	req, _ := http.NewRequest("GET", url, nil)
	req.Header.Set("User-Agent", f.userAgent)
	resp, err := client.Do(req)
	fmt.Println(resp)

	defer func() {
		resp.Body.Close()
		f.chDone <- true
	}()

	if err != nil || resp.StatusCode != 200 {
		f.chFailed <- url
		return
	}
}

func (f *Fetcher) Fetch() {
	for _, url := range f.urls {
		go f.fetchUrl(url)
	}

	for i := 0; i < len(f.urls); {
		select {
		case url := <-f.chFailed:
			f.failedUrls = append(f.failedUrls, url)
		case <-f.chDone:
			i++
		}
	}
}

func (f *Fetcher) GetResults() map[string]string {
	return f.results
}

func (f *Fetcher) GetFailedUrls() []string {
	return f.failedUrls
}
