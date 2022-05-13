package mafio

import (
	"strings"
	"testing"
)

func TestWriter(t *testing.T) {
	t.Run("write comments to a file", func(t *testing.T) {
		comments := []string{"# comment 1", "# comment 2"}
		got := new(strings.Builder)
		WriteComments(got, comments)
		want := `# comment 1
# comment 2
`
		if got.String() != want {
			t.Errorf("got %q is not the same as %q", got, want)
		}
	})

	t.Run("write headers to a file", func(t *testing.T) {
		headers := []string{"Foo", "Bar", "Baz"}
		got := new(strings.Builder)
		WriteHeader(got, headers)
		want := "Foo\tBar\tBaz\n"
		if got.String() != want {
			t.Errorf("got %q is not the same as %q", got, want)
		}
	})

	t.Run("write comments and headers to a file", func(t *testing.T) {
		comments := []string{"# comment 1", "# comment 2"}
		headers := []string{"Foo", "Bar", "Baz"}
		got := new(strings.Builder)
		WriteComments(got, comments)
		WriteHeader(got, headers)
		want := "# comment 1\n# comment 2\nFoo\tBar\tBaz\n"
		if got.String() != want {
			t.Errorf("got %q is not the same as %q", got, want)
		}
	})

	t.Run("make output fields from headers and row", func(t *testing.T) {
		row_map := map[string]string{"Foo": "1", "Bar": "2", "Baz": "3", "Buzz": "4"}
		headers := []string{"Foo", "Bar", "Baz"}
		got := MakeRowFields(headers, row_map)
		want := []string{"1", "2", "3"}

		if len(got) != len(want) {
			t.Errorf("got %q is not the same length as %q", got, want)
		}

		for i, v := range want {
			if v != got[i] {
				t.Errorf("got %q want %q", got[i], v)
			}
		}
	})

	t.Run("write output from headers, comments, and rows", func(t *testing.T) {
		rows := []map[string]string{
			{"Foo": "a", "Bar": "b", "Baz": "c", "Buzz": "d"}, // this extra field wont be in the output
			{"Foo": "x", "Bar": "y", "Baz": "z"},
			{"Foo": "zz", "Bar": "yy", "Baz": "bb"},
		}
		headers := []string{"Foo", "Bar", "Baz"}
		comments := []string{"# comment 1", "# comment 2"}
		got := new(strings.Builder)
		writer := NewMafWriter(got, headers, comments)

		for _, row := range rows {
			fields := MakeRowFields(writer.headers, row)
			writer.WriteRow(fields)
		}

		w := `# comment 1
# comment 2
Foo\tBar\tBaz
a\tb\tc
x\ty\tz
zz\tyy\tbb
`
		var want string = strings.ReplaceAll(w, `\t`, "\t")

		if got.String() != want {
			t.Errorf("got %q is not the same as %q", got, want)
		}
	})

}
