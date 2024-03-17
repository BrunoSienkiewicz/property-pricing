package fetch

import (
	"fmt"
	// "log"
	"strconv"
)

const (
	pageUrl   = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/"
	userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0" +
		"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
)

type ListingFetcher struct {
	Fetcher
}

func (f *ListingFetcher) processResults() {
	for url, body := range f.results {
		// process body
		_ = url
		_ = body
	}
}

func FetchListings(city string, pages int) map[string]string {
	var pagesUrls []string
	for i := 1; i <= pages; i++ {
		url := pageUrl + city + "/?page=" + strconv.Itoa(i)
		pagesUrls = append(pagesUrls, url)
	}

	listingFetcher := ListingFetcher{Fetcher: *NewFetcher(userAgent, pagesUrls)}
	listingFetcher.Fetch()

	results := listingFetcher.GetResults()
	failedUrls := listingFetcher.GetFailedUrls()

	if len(failedUrls) > 0 {
		fmt.Println("Could not fetch the following urls:", failedUrls)
		// log.Println("Could not fetch the following urls:", failedUrls)
	}

	return results
}
