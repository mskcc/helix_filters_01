package main

// USAGE:
// filterUncalledMutations /path/to/data_mutations.txt --output-dir /path/to/outputdir
// NOTE: creates directory "output" and places files in there to avoid filename collision in pwd

import (
	"io"
	"fmt"
	"helix/mafio"
	"log"
	"os"
	"path/filepath"
	"github.com/alecthomas/kong"
)

// primary method for running the uncalled filter methods on the supplied input / output files
func run(inputFilepath string, mutsFilepath string, uncalledFilepath string) error {
	// open input and output files
	inputFile, err2 := os.Open(inputFilepath)
	if err2 != nil {
		log.Fatalln("Couldn't open the file", err2)
	}
	defer inputFile.Close()

	outputMutsFile, err3 := os.Create(mutsFilepath)
	if err3 != nil {
		log.Fatalln("Couldn't open the file", err3)
	}
	defer outputMutsFile.Close()

	outputUncalledFile, err4 := os.Create(uncalledFilepath)
	if err4 != nil {
		log.Fatalln("Couldn't open the file", err4)
	}
	defer outputUncalledFile.Close()

	// get comments and headers from input
	comment_reader, err5 := os.Open(inputFilepath)
	if err5 != nil {
		log.Fatalln("Couldn't open the file", err5)
	}
	defer inputFile.Close()

	comments := mafio.ParseComments(comment_reader)

	header_reader, err6 := os.Open(inputFilepath)
	if err6 != nil {
		log.Fatalln("Couldn't open the file", err6)
	}
	defer header_reader.Close()
	headers := mafio.ParseHeader(header_reader)

	// initalize the maf reader
	mafReader := mafio.NewMafReader(inputFile, comments, headers)

	// initialize the maf writers
	mutsWriter := mafio.NewMafWriter(outputMutsFile, headers, comments)
	mutsUncalledWriter := mafio.NewMafWriter(outputUncalledFile, headers, comments)

	// iterate over rows in the maf file
	for {
		row, err := mafReader.ReadRow()
		if row == nil {
			break
		}
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatal(err)
			break
		}
		// convert row to a Mutation
		mutation := mafio.MutationFromMap(row)
		// check if the mutation is "uncalled" or not
		isUncalled := mafio.IsUncalledMutationUpdate(&mutation)
		fields := mafio.MakeRowFields(headers, mutation.ToMap())
		// write the row to the corresponding file
		if isUncalled {
			mutsUncalledWriter.WriteRow(fields)
		} else {
			mutsWriter.WriteRow(fields)
		}
	}

	return nil
}

// struct to hold the command line parsing options
type CLI struct {
	InputFilepath string `help:"path to input mutations file" arg:""`
	OutputDir string `help:"path to output directory" default:"./output"` // --output-dir
	MutsFilename string `default:"data_mutations_extended.txt" help:"output filename for called mutations"` // --muts-filename
	UncalledFilename string `default:"data_mutations_uncalled.txt" help:"output filename for uncalled mutations"` // --uncalled-filename
}

// method to run the script with the CLI args; gets invoked by `ctx.Run()`
func (cli *CLI) Run () error {
	outputDir := cli.OutputDir

	err := os.MkdirAll(outputDir, os.ModePerm)
	if err != nil {
		fmt.Printf("Could not create directory %v\n", outputDir)
		log.Fatalln("Couldn't create directory the file", err)
	}

	inputFilepath := cli.InputFilepath
	mutsFilename := cli.MutsFilename
	uncalledFilename := cli.UncalledFilename

	mutsFilepath := filepath.Join(outputDir, mutsFilename)
	uncalledFilepath := filepath.Join(outputDir, uncalledFilename)

	err = run(inputFilepath, mutsFilepath, uncalledFilepath)
	return err
}

func main() {
	var cli CLI

	ctx := kong.Parse(&cli,
		kong.Name("Filter Uncalled Mutations"),
		kong.Description("Program for splitting mutations files into called and uncalled mutations."))

	ctx.FatalIfErrorf(ctx.Run())
}
