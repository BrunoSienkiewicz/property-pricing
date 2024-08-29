package fetch

import (
	"io/ioutil"
	"net/http"
)

type Fetcher[T any] struct {
	userAgent  string
	urls       []string
	urls_body  map[string]string
	results    map[string]T
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

func NewFetcher[T any](userAgent string, urls []string) *Fetcher[T] {
	return &Fetcher[T]{
		userAgent: userAgent,
		urls:      urls,
		urls_body: make(map[string]string),
		results:   make(map[string]T),
		chFailed:  make(chan string),
		chDone:    make(chan bool),
	}
}

func (f *Fetcher[T]) fetchUrl(url string) {
	client := &http.Client{}
	req, _ := http.NewRequest("GET", url, nil)
	req.Header.Set("User-Agent", f.userAgent)
	resp, err := client.Do(req)

	defer func() {
		content, err := ioutil.ReadAll(resp.Body)

		if err != nil {
			f.chFailed <- url
			return
		}

		f.urls_body[url] = string(content)
		resp.Body.Close()
		f.chDone <- true
	}()

	if err != nil || resp.StatusCode != 200 {
		f.chFailed <- url
		return
	}
}

func (f *Fetcher[T]) Fetch() {
	for _, url := range f.urls {
		go f.fetchUrl(url)
	}

	for i := 0; i < len(f.urls); {
		select {
		case url := <-f.chFailed:
			f.failedUrls = append(f.failedUrls, url)
			i++
		case <-f.chDone:
			i++
		}
	}
}

func (f *Fetcher[T]) GetResults() map[string]T {
	return f.results
}

func (f *Fetcher[T]) GetFailedUrls() []string {
	return f.failedUrls
}
