package main

// USAGE:
// filterUncalledMutations /path/to/data_mutations.txt /path/to/outputdir
// NOTE: creates directory "output" and places files in there to avoid filename collision in pwd

import (
	"io"
	"fmt"
	"helix/mafio"
	"log"
	"os"
	"path/filepath"
)

var _defaultOutputDir string = "output"
var _defaultDataMutsFilename string = "data_clinical_mutations.txt"
var _defaultDataMutsUncalledFilename string = "data_mutations_uncalled.txt"

func main() {
	// get CLI args
	args := os.Args[1:]
	inputFilepath := args[0]
	var outputDir string
	if len(args) > 1 {
		outputDir = args[1]
	} else  {
		outputDir = _defaultOutputDir
	}
	outputMutsPath := filepath.Join(outputDir, _defaultDataMutsFilename)
	outputUncalledPath := filepath.Join(outputDir, _defaultDataMutsUncalledFilename)

	// make output path
	err := os.MkdirAll(outputDir, os.ModePerm)
	if err != nil {
		fmt.Printf("Could not create directory %v\n", outputDir)
		log.Fatalln("Couldn't create directory the file", err)
	}

	// open input and output files
	inputFile, err2 := os.Open(inputFilepath)
	if err2 != nil {
		log.Fatalln("Couldn't open the file", err2)
	}
	defer inputFile.Close()

	outputMutsFile, err3 := os.Create(outputMutsPath)
	if err3 != nil {
		log.Fatalln("Couldn't open the file", err3)
	}
	defer outputMutsFile.Close()

	outputUncalledFile, err4 := os.Create(outputUncalledPath)
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
}
