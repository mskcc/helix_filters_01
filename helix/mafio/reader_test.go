package mafio

import (
	"io"
	"os"
	"fmt"
	"log"
	"strings"
	"testing"
	"github.com/google/go-cmp/cmp"
	"github.com/mitchellh/mapstructure"
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
// - called mut
// - called mut (should be uncalled, fillout == true)
// - called mut (should be uncalled, t_alt_count == 0)
var _mafStr string = `#comment 1
#comment2
Mutation_Status\tt_ref_count\tt_alt_count\tis_fillout\tFoo
CALLED\t10\t10\tFalse\tfoo1
CALLED\t10\t10\tTrue\tfoo2
CALLED\t10\t0\tFalse\tfoo3
`
var mafStr string = strings.ReplaceAll(_mafStr, `\t`, "\t")

func TestReader(t *testing.T) {

	t.Run("parse the comment lines", func(t *testing.T) {
		fmt.Printf("")
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
		file, err := os.Open(test_file)
		if err != nil {
			log.Fatalln("Couldn't open the file", err)
		}
		defer file.Close()

		m := NewMafReader(file, []string{"# comment1", "# comment2"}, []string{"SampleID", "Foo", "Bar", "Baz", "RefCount", "AltCount"})

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
		file, err := os.Open(test_file)
		if err != nil {
			log.Fatalln("Couldn't open the file", err)
		}
		defer file.Close()

		m := NewMafReader(file, []string{"# comment1", "# comment2"}, []string{"SampleID", "Foo", "Bar", "Baz", "RefCount", "AltCount"})
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


// Tests for reading mutations
	t.Run("Read mutations from maf format string", func(t *testing.T) {
		// read the comments
		comment_reader := strings.NewReader(mafStr)
		comments := ParseComments(comment_reader)
		comments_wanted := []string{"#comment 1", "#comment2"}
		if diff := cmp.Diff(comments_wanted, comments); diff != "" {
			t.Errorf("got vs want mismatch (-want +got):\n%s", diff)
		}

		// read the headers
		header_reader := strings.NewReader(mafStr)
		headers := ParseHeader(header_reader)
		headers_wanted := []string{"Mutation_Status", "t_ref_count", "t_alt_count", "is_fillout", "Foo"}
		if diff := cmp.Diff(headers_wanted, headers); diff != "" {
			t.Errorf("got vs want mismatch (-want +got):\n%s", diff)
		}

		// initalize maf reader
		mafStr_reader := strings.NewReader(mafStr)
		reader := NewMafReader(mafStr_reader, comments, headers)

		// read all rows and mutations
		var rows []map[string]string
		var mutations []Mutation
		for {
			row, err := reader.ReadRow()
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
			mutation := MutationFromMap(row)
			rows = append(rows, row)
			mutations = append(mutations, mutation)
		}
		rows_wanted := []map[string]string{
			{
			"Mutation_Status": "CALLED",
			"is_fillout":      "False",
			"t_alt_count":     "10",
			"t_ref_count":     "10",
			"Foo": "foo1",
			},
			{
			"Mutation_Status": "CALLED",
			"is_fillout":      "True",
			"t_alt_count":     "10",
			"t_ref_count":     "10",
			"Foo": "foo2",
			},
			{
			"Mutation_Status": "CALLED",
			"is_fillout":      "False",
			"t_alt_count":     "0",
			"t_ref_count":     "10",
			"Foo": "foo3",
			},
		}
		if diff := cmp.Diff(rows_wanted, rows); diff != "" {
			t.Errorf("got vs want mismatch (-want +got):\n%s", diff)
		}

		mutations_wanted := []Mutation{
			Mutation{
				TRefCount: 10,
				TAltCount: 10,
				MutationStatus: "CALLED",
				IsFillout: false,
				SourceMap: map[string]string{
					"Mutation_Status": "CALLED",
					"is_fillout":      "False",
					"t_alt_count":     "10",
					"t_ref_count":     "10",
					"Foo": "foo1",
				},
				Metadata: mapstructure.Metadata{
					Keys:   []string{"t_ref_count", "t_alt_count", "Mutation_Status", "is_fillout"},
					Unused: []string{"Foo"},
					Unset:  []string{"Metadata", "SourceMap"},
				},
			},
			Mutation{
				TRefCount: 10,
				TAltCount: 10,
				MutationStatus: "CALLED",
				IsFillout: true,
				SourceMap: map[string]string{
					"Mutation_Status": "CALLED",
					"is_fillout":      "True",
					"t_alt_count":     "10",
					"t_ref_count":     "10",
					"Foo": "foo2",
				},
				Metadata: mapstructure.Metadata{
					Keys:   []string{"t_ref_count", "t_alt_count", "Mutation_Status", "is_fillout"},
					Unused: []string{"Foo"},
					Unset:  []string{"Metadata", "SourceMap"},
				},
			},
			Mutation{
				TRefCount: 10,
				TAltCount: 0,
				MutationStatus: "CALLED",
				IsFillout: false,
				SourceMap: map[string]string{
					"Mutation_Status": "CALLED",
					"is_fillout":      "False",
					"t_alt_count":     "0",
					"t_ref_count":     "10",
					"Foo": "foo3",
				},
				Metadata: mapstructure.Metadata{
					Keys:   []string{"t_ref_count", "t_alt_count", "Mutation_Status", "is_fillout"},
					Unused: []string{"Foo"},
					Unset:  []string{"Metadata", "SourceMap"},
				},
			},
		}
		if diff := cmp.Diff(mutations_wanted, mutations); diff != "" {
			t.Errorf("got vs want mismatch (-want +got):\n%s", diff)
		}





	})

}
