package main

// USAGE:
// newCaseList <type> <studyIdentifier> Sample1,Sample2,...

import (
	"fmt"
	"helix/portal"
	"log"
	"os"
	"strings"
)

func main() {
	args := os.Args[1:]

	typ_str := args[0]
	studyIdentifier := args[1]
	ids_str := args[2]

	var typ portal.CaseListType

	if typ_str == "all" {
		typ = portal.CaseListTypeAll
	} else if typ_str == "cnaseq" {
		typ = portal.CaseListTypeCNASeq
	} else if typ_str == "cna" {
		typ = portal.CaseListTypeCNA
	} else if typ_str == "seq" {
		typ = portal.CaseListTypeSeq
	} else {
		log.Fatalf("Invalid type: %q. Use one of 'all', 'cna', 'seq', or 'cnaseq'", typ_str)
	}

	ids := strings.Split(ids_str, ",")

	c := portal.NewCaseList(studyIdentifier, ids, typ)
	lines := c.ToLines()
	for _, line := range lines {
		fmt.Println(line)
	}

}
