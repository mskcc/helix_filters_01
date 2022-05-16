package mafio

import (
	"testing"
	// "fmt"
	// "strings"
	"github.com/google/go-cmp/cmp"
	"github.com/mitchellh/mapstructure"
)

func TestMutations(t *testing.T) {
	t.Run("Test Mutation initialization", func(t *testing.T) {
		// source data
		data := map[string]string{
			"t_ref_count":     "11",
			"t_alt_count":     "5",
			"Mutation_Status": "CALLED",
			"is_fillout":         "True",
			"foo":             "bar", // extraneous key
		}

		// expected values
		var t_ref_count int64 = 11
		var t_alt_count int64 = 5
		var Mutation_Status = "CALLED"
		var is_fillout bool = true
		metadata := mapstructure.Metadata{
			Keys:   []string{"t_ref_count", "t_alt_count", "Mutation_Status", "is_fillout"},
			Unused: []string{"foo"},
			Unset:  []string{"Metadata", "SourceMap"}, // these get sorted by the MutationFromMap method
		}

		// convert to mutation type
		got := MutationFromMap(data)

		want := Mutation{
			TRefCount:      t_ref_count,
			TAltCount:      t_alt_count,
			MutationStatus: Mutation_Status,
			IsFillout:      is_fillout,
			Metadata:       metadata,
			SourceMap:      data,
		}
		// if !cmp.Equal(got, want) {
		// 	t.Errorf("got %v is not the same as %v", got, want)
		// }
		if diff := cmp.Diff(want, got); diff != "" {
			t.Errorf("got vs want mismatch (-want +got):\n%s", diff)
		}
	})

	t.Run("Test Mutation convert back to map", func(t *testing.T) {
		data := map[string]string{
			"t_ref_count":     "11",
			"t_alt_count":     "5",
			"Mutation_Status": "CALLED",
			"is_fillout":         "True",
			"foo":             "bar", // extraneous key
		}
		mutation := MutationFromMap(data)
		got := mutation.ToMap()
		want := map[string]string{
			"t_ref_count":     "11",
			"t_alt_count":     "5",
			"Mutation_Status": "CALLED",
			"is_fillout":         "True",
			"foo":             "bar",
		}
		// fmt.Printf("\n\n%v\n\n", got)
		if !cmp.Equal(got, want) {
			// https://faun.pub/golangs-fmt-sprintf-and-printf-demystified-4adf6f9722a2
			t.Errorf("got %v is not the same as %v", got, want)
		}
	})


	t.Run("Test Mutation update uncalled status", func(t *testing.T) {
		mutation := Mutation{
			TRefCount:      11,
			TAltCount:      5,
			MutationStatus: "CALLED",
			IsFillout:      false,
			Metadata:       mapstructure.Metadata{},
			SourceMap:      map[string]string{},
		}

		got := mutation
		got.SetUncalled()

		want := Mutation{
			TRefCount:      11,
			TAltCount:      5,
			MutationStatus: "UNCALLED",
			IsFillout:      false,
			Metadata:       mapstructure.Metadata{},
			SourceMap:      map[string]string{},
		}
		if !cmp.Equal(got, want) {
			t.Errorf("got %v is not the same as %v", got, want)
		}
	})


	t.Run("Test Mutation convert to map after updating status", func(t *testing.T) {
		mutation := Mutation{
			TRefCount:      11,
			TAltCount:      5,
			MutationStatus: "CALLED",
			IsFillout:      false,
			Metadata:       mapstructure.Metadata{},
			SourceMap:      map[string]string{"foo":"bar"},
		}

		mutation.SetUncalled()

		got := mutation.ToMap()

		want := map[string]string{
			"t_ref_count":     "11",
			"t_alt_count":     "5",
			"Mutation_Status": "UNCALLED",
			"is_fillout":         "False",
			"foo":             "bar",
		}
		if !cmp.Equal(got, want) {
			t.Errorf("got %#v is not the same as %#v", got, want)
		}
	})
}
