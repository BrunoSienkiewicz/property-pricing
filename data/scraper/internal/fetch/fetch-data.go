package fetch

import (
	"fmt"
	// "io/ioutil"
	// "net/http"
	"strings"

	types "github.com/BrunoSienkiewicz/Property_pricing/data/scraper/internal/types"
)

type DataFetcher struct {
	Fetcher[types.Listing]
}

func (f *DataFetcher) processResults() {
	for url, body := range f.urls_body {
		start := "\"props\":\""
		// sep := ":"

		startIdx := strings.Index(body, start)
		if startIdx == -1 {
			f.chFailed <- url
			return
		}

		startIdx += len(start)
		endIdx := strings.Index(body[startIdx:], "</script>")

		if endIdx == -1 {
			f.chFailed <- url
			return
		}

		//parse content between startIdx and endIdx
		content := body[startIdx : startIdx+endIdx]
		fmt.Println(content)
	}
}

func FetchData(urls []string) map[string]types.Listing {
	dataFetcher := DataFetcher{Fetcher: *NewFetcher[types.Listing](userAgent, urls)}
	dataFetcher.Fetch()
	dataFetcher.processResults()

	return dataFetcher.GetResults()
}
