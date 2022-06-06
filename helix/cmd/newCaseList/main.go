package main

// USAGE:
// newCaseList <type> <studyIdentifier> Sample1,Sample2,... > case_list.txt

import (
	"fmt"
	"github.com/alecthomas/kong"
	"helix/portal"
	"log"
	"strings"
)

// primary run function for the script
func run(typeLabel string, studyIdentifier string, ids []string) error {
	// check the type of case list required
	var typ portal.CaseListType
	if typeLabel == "all" {
		typ = portal.CaseListTypeAll
	} else if typeLabel == "cnaseq" {
		typ = portal.CaseListTypeCNASeq
	} else if typeLabel == "cna" {
		typ = portal.CaseListTypeCNA
	} else if typeLabel == "seq" {
		typ = portal.CaseListTypeSeq
	} else {
		log.Fatalf("Invalid type: %q. Use one of 'all', 'cna', 'seq', or 'cnaseq'", typeLabel)
	}

	c := portal.NewCaseList(studyIdentifier, ids, typ)
	lines := c.ToLines()
	for _, line := range lines {
		fmt.Println(line)
	}

	return nil
}

// struct to hold the command line parsing options
type CLI struct {
	TypeLabel       string `help:"type of case list to create [all, cnaseq, cna, seq]" arg:""`
	StudyIdentifier string `help:"Study identifier" arg:""`
	Ids             string `help:"comma-delimited list of id's to add to the case list" arg:""`
}

// method to run the script with the CLI args; gets invoked by `ctx.Run()`
func (cli *CLI) Run() error {
	ids_str := cli.Ids
	ids := strings.Split(ids_str, ",")
	typeLabel := cli.TypeLabel
	studyIdentifier := cli.StudyIdentifier

	err := run(typeLabel, studyIdentifier, ids)
	return err
}

func main() {
	var cli CLI

	ctx := kong.Parse(&cli,
		kong.Name("Create Case List File"),
		kong.Description("Program for creating a case list file for cBioPortal."))

	ctx.FatalIfErrorf(ctx.Run())
}
