package mafio

import (
	"io"
	"log"
	"strings"
	"testing"
)

// fixtures for test cases
var s1 string = `#comment 1
#comment2
Foo\tBar\tBaz
1\t2\t3
`
// need to convert \t to real tabs
var s string = strings.ReplaceAll(s1, `\t`, "\t")
var test_file string = "../testdata/tsv/test.tsv"

// NOTE: update this as more fields are added to Mutation
var _mafStr string = `#comment 1
#comment2
Mutation_Status\tt_ref_count\tt_alt_count\tis_fillout
`


func TestReader(t *testing.T) {

	t.Run("parse the comment lines", func(t *testing.T) {
		reader := strings.NewReader(s)
		got := ParseComments(reader)
		want := []string{"#comment 1", "#comment2"}

		if len(got) != len(want) {
			t.Errorf("got %q is not the same length as %q", got, want)
		}

		for i, v := range want {
			if v != got[i] {
				t.Errorf("got %q want %q", got[i], v)
			}
		}
	})

	t.Run("parse the header lines", func(t *testing.T) {
		reader := strings.NewReader(s)
		got := ParseHeader(reader)
		want := []string{"Foo", "Bar", "Baz"}

		if len(got) != len(want) {
			t.Errorf("got %q is not the same length as %q", got, want)
		}

		for i, v := range want {
			if v != got[i] {
				t.Errorf("got %q want %q", got[i], v)
			}
		}
	})

	t.Run("convert lists of keys and values into a map", func(t *testing.T) {
		keys := []string{"Foo", "Bar"} // headers
		values := []string{"1", "2"}   // row

		got := MakeMap(keys, values)
		want := map[string]string{"Foo": "1", "Bar": "2"}

		if len(got) != len(want) {
			t.Errorf("got %q is not the same length as %q", got, want)
		}

		for k, v := range want {
			if v != got[k] {
				t.Errorf("got %q want %q", got[k], v)
			}
		}
	})

	t.Run("read a tab delimited file", func(t *testing.T) {
		m := NewMafReader(test_file)

		wanted_comments := []string{"# comment1", "# comment2"}
		wanted_headers := []string{"SampleID", "Foo", "Bar", "Baz", "RefCount", "AltCount"}

		if len(m.comments) != len(wanted_comments) {
			t.Errorf("got %q is not the same length as %q", m.comments, wanted_comments)
		}

		for i, v := range wanted_comments {
			if v != m.comments[i] {
				t.Errorf("got %q want %q", m.comments[i], v)
			}
		}

		if len(m.headers) != len(wanted_headers) {
			t.Errorf("got %q is not the same length as %q", m.headers, wanted_headers)
		}

		for i, v := range wanted_headers {
			if v != m.headers[i] {
				t.Errorf("got %q want %q", m.headers[i], v)
			}
		}

		// read first row
		got, err := m.ReadRow()
		want := map[string]string{"SampleID": "Sample1", "RefCount": "30", "AltCount": "100", "Foo": "a", "Bar": "b", "Baz": "c"}
		if len(got) != len(want) {
			t.Errorf("got %q is not the same length as %q", got, want)
		}
		for k, v := range want {
			if v != got[k] {
				t.Errorf("got %q want %q", got[k], v)
			}
		}
		if err != nil {
			log.Fatal(err)
		}

		// read second row
		got2, err2 := m.ReadRow()
		want2 := map[string]string{"SampleID": "Sample2", "RefCount": "25", "AltCount": "250", "Foo": "x", "Bar": "y", "Baz": "z"}
		if len(got2) != len(want2) {
			t.Errorf("got %q is not the same length as %q", got2, want2)
		}
		for k, v := range want2 {
			if v != got2[k] {
				t.Errorf("got %q want %q", got2[k], v)
			}
		}
		if err2 != nil {
			log.Fatal(err2)
		}

		// read third row
		got3, err3 := m.ReadRow()
		want3 := map[string]string{"SampleID": "Sample3", "RefCount": "375", "AltCount": "0", "Foo": "zz", "Bar": "yy", "Baz": "bb"}
		if len(got3) != len(want3) {
			t.Errorf("got %q is not the same length as %q", got3, want3)
		}
		for k, v := range want3 {
			if v != got3[k] {
				t.Errorf("got %q want %q", got3[k], v)
			}
		}
		if err3 != nil {
			log.Fatal(err3)
		}
	})

	t.Run("iterate over rows in a tab delimited file", func(t *testing.T) {
		m := NewMafReader(test_file)
		var rows []map[string]string

		for {

			// Read each row from csv
			row, err := m.ReadRow()
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

			rows = append(rows, row)
		}

		want := []map[string]string{
			{"SampleID": "Sample1", "RefCount": "30", "AltCount": "100", "Foo": "a", "Bar": "b", "Baz": "c"},
			{"SampleID": "Sample2", "RefCount": "25", "AltCount": "250", "Foo": "x", "Bar": "y", "Baz": "z"},
			{"SampleID": "Sample3", "RefCount": "375", "AltCount": "0", "Foo": "zz", "Bar": "yy", "Baz": "bb"},
		}

		if len(rows) != len(want) {
			t.Errorf("got %q is not the same length as %q", rows, want)
		}
		for i, mapp := range want {
			for k, v := range mapp {
				if v != rows[i][k] {
					t.Errorf("got %q want %q", rows[i][k], v)
				}
			}
		}
	})

}
