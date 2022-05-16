package mafio

import (
	"bufio"
	"encoding/csv"
	"io"
	"log"
	// "os"
)

type MafReader struct {
	headers  []string
	comments []string
	reader   *csv.Reader
}

func (m *MafReader) ReadRow() (map[string]string, error) {
	// Read a row from csv
	row, err := m.reader.Read() // csv.NewReader(file)

	// TODO: how should the errors be handled here?
	if err == io.EOF {
		return nil, err
	}
	if err != nil {
		return nil, err
	}

	row_map := MakeMap(m.headers, row)
	return row_map, err
}

func NewMafReader(file io.Reader, comments []string, headers []string) MafReader {
	// filepath string
	// file, err := os.Open(filepath)
	// if err != nil {
	// 	log.Fatalln("Couldn't open the file", err)
	// }
	// TODO: WHEN TO CALL THIS??
	// defer file.Close() // err "read test.tsv: file already closed"
	// comments := ParseComments(file)
	// reset the input file cursor
	// file.Seek(0, 0)
	// headers := ParseHeader(file)
	// file.Seek(0, 0)

	reader := csv.NewReader(file)
	reader.Comma = delim
	reader.Comment = commentChar

	// skip the header
	_, header_err := reader.Read()
	if header_err == io.EOF {
		log.Fatal(header_err)
	}

	mafReader := MafReader{headers, comments, reader}

	return mafReader
}

func ParseComments(file io.Reader) []string {
	// get the comments from the file
	// need to initialize a buffer for the scanner that is larger than the default 64KB size
	const maxCapacity = 2048 * 1024 // 2Mb
	buf := make([]byte, maxCapacity)

	scanner := bufio.NewScanner(file)
	scanner.Buffer(buf, maxCapacity)

	var commentLines []string

	for scanner.Scan() {
		var line string
		line = scanner.Text()

		if len(line) > 0 && string(line[0]) == string(commentChar) {
			commentLines = append(commentLines, line)
		} else {
			break
		}

	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return commentLines
}

func ParseHeader(file io.Reader) []string {
	// get the headers from the first line
	reader := csv.NewReader(file)
	reader.Comma = delim         // from settings
	reader.Comment = commentChar // from settings
	var headers []string
	headers, header_err := reader.Read()
	if header_err == io.EOF {
		log.Fatal(header_err)
	}

	return headers
}

func MakeMap(keys []string, values []string) map[string]string {
	// make empty map to hold row data
	row_map := make(map[string]string)

	// parse the row data into the map
	for i, key := range keys {
		row_map[key] = values[i]
	}
	return row_map
}
