package main

// USAGE:
// updateCaseList cases.txt Sample3,Sample4 > new_case_list.txt

import (
	"fmt"
	"helix/portal"
	"log"
	"os"
	"strings"
	"github.com/alecthomas/kong"
)

// primary run method for the script
func run (inputFilepath string, ids []string) error {
	// open the intput file
	file, err := os.Open(inputFilepath)
	if err != nil {
		log.Fatalln("Couldn't open the file", err)
	}
	defer file.Close()

	// load the case list data
	c := portal.LoadCaseList(file)

	// add the new id's to the case list data
	c.AddIds(ids)

	// create and print the new case list lines
	lines := c.ToLines()
	for _, line := range lines {
		fmt.Println(line)
	}

	return nil
}

// struct to hold the command line parsing options
type CLI struct {
	InputFilepath string `help:"path to input case list file" arg:""`
	Ids string `help:"comma-delimited list of id's to add to the case list" arg:""`
}

// method to run the script with the CLI args; gets invoked by `ctx.Run()`
func (cli *CLI) Run () error {
	ids_str := cli.Ids
	ids := strings.Split(ids_str, ",")
	inputFilepath := cli.InputFilepath
	err := run(inputFilepath, ids)
	return err
}

func main() {
	var cli CLI

	ctx := kong.Parse(&cli,
		kong.Name("Update Case List File"),
		kong.Description("Program for updating a case list file with extra sample ID's."))

	ctx.FatalIfErrorf(ctx.Run())
}
