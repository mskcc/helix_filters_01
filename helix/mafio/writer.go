package mafio

import (
    "io"
    "fmt"
    "log"
    "encoding/csv"
)

type MafWriter struct {
    headers []string
    comments []string
    file io.Writer
    writer *csv.Writer
}

func (m *MafWriter) WriteRow (row []string) {
    m.writer.Write(row)
    // Write any buffered data to the underlying writer
    m.writer.Flush()
    if err := m.writer.Error(); err != nil {
        log.Fatal(err)
    }
}

func NewMafWriter(file io.Writer, headers []string, comments []string) MafWriter {
    WriteComments(file, comments)
    WriteHeader(file, headers)
    writer := csv.NewWriter(file)
    writer.Comma = delim // from settings
    writer.UseCRLF = false
    m := MafWriter{headers, comments, file, writer}
    return m
}

// writes the comment lines to the output file
func WriteComments(file io.Writer, comments []string) {
        for _, comment := range comments {
            _, err := fmt.Fprintln(file, comment)
            if err != nil {
                log.Fatal(err)
            }
        }
}

// writes the table headers to the csv file
func WriteHeader(file io.Writer, headers []string) {
    // write out the headers
    writer := csv.NewWriter(file)
    writer.Comma = delim // from settings
    writer.UseCRLF = false
    if err := writer.Write(headers); err != nil {
            log.Fatalln("error writing headers to file:", err)
        }

    // Write any buffered data to the underlying writer
    writer.Flush()
    if err := writer.Error(); err != nil {
        log.Fatal(err)
    }
}

// generates the fields to be written on the output csv line based on the header and row mappings
func MakeRowFields (headers []string, row map[string]string) []string {
    var output_row []string
    for _, header := range headers {
        output_row = append(output_row, row[header])
    }
    return output_row
}
