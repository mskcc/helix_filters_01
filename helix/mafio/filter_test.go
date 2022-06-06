package mafio

import (
	"testing"
	// "fmt"
	"github.com/google/go-cmp/cmp"
	"github.com/mitchellh/mapstructure"
)

func TestFilters(t *testing.T) {
	t.Run("Test mutation filtering IsUncalledFilter", func(t *testing.T) {
		// a mutation is considered "Uncalled" if t_alt_count == 0 or is_fillout = True
		// an "uncalled" mutation should be "kept" for the data_mutations_uncalled.txt file

		// source data
		mutation := Mutation{
			TRefCount:      10,
			TAltCount:      0, // should be kept in uncalled file
			MutationStatus: "",
			IsFillout:      false,
			Metadata:       mapstructure.Metadata{},
			SourceMap:      map[string]string{},
		}
		// fmt.Printf("\n\n%v\n\n", mutation)
		got := IsUncalledFilter(&mutation)
		want := true
		if !cmp.Equal(got, want) {
			t.Errorf("got %v is not the same as %v", got, want)
		}

		// should not be kept in uncalled file
		mutation = Mutation{
			TRefCount:      10,
			TAltCount:      10,
			MutationStatus: "",
			IsFillout:      false,
			Metadata:       mapstructure.Metadata{},
			SourceMap:      map[string]string{},
		}
		got = IsUncalledFilter(&mutation)
		want = false
		if !cmp.Equal(got, want) {
			t.Errorf("got %v is not the same as %v", got, want)
		}

		mutation = Mutation{
			TRefCount:      10,
			TAltCount:      10,
			MutationStatus: "",
			IsFillout:      true, // should be kept in uncalled file
			Metadata:       mapstructure.Metadata{},
			SourceMap:      map[string]string{},
		}
		got = IsUncalledFilter(&mutation)
		want = true
		if !cmp.Equal(got, want) {
			t.Errorf("got %v is not the same as %v", got, want)
		}
	})

	t.Run("Test mutation filtering IsUncalledMutationUpdate", func(t *testing.T) {
		// a mutation is considered "Uncalled" if t_alt_count == 0 or is_fillout = True
		// an "uncalled" mutation should be "kept" for the data_mutations_uncalled.txt file

		// source data; is Uncalled
		mutation := Mutation{
			TRefCount:      10,
			TAltCount:      0, // should be kept in uncalled file
			MutationStatus: "",
			IsFillout:      false,
			Metadata:       mapstructure.Metadata{},
			SourceMap:      map[string]string{},
		}
		got := IsUncalledMutationUpdate(&mutation)
		want := true
		if !cmp.Equal(got, want) {
			t.Errorf("got %v is not the same as %v", got, want)
		}

		// check that the Mutation was updated
		wantedMutation := Mutation{
			TRefCount:      10,
			TAltCount:      0,
			MutationStatus: "UNCALLED", // updated value
			IsFillout:      false,
			Metadata:       mapstructure.Metadata{},
			SourceMap:      map[string]string{},
		}
		if !cmp.Equal(wantedMutation, mutation) {
			t.Errorf("got %v is not the same as %v", wantedMutation, mutation)
		}

		// test that a non-uncalled Mutation does not get changed
		mutation = Mutation{
			TRefCount:      10,
			TAltCount:      10,
			MutationStatus: "CALLED", // should not change
			IsFillout:      false,
			Metadata:       mapstructure.Metadata{},
			SourceMap:      map[string]string{},
		}
		got = IsUncalledMutationUpdate(&mutation)
		want = false
		if !cmp.Equal(got, want) {
			t.Errorf("got %v is not the same as %v", got, want)
		}

		// check that the Mutation was NOT updated
		wantedMutation = Mutation{
			TRefCount:      10,
			TAltCount:      10,
			MutationStatus: "CALLED", // updated value
			IsFillout:      false,
			Metadata:       mapstructure.Metadata{},
			SourceMap:      map[string]string{},
		}
		if !cmp.Equal(wantedMutation, mutation) {
			t.Errorf("got %v is not the same as %v", wantedMutation, mutation)
		}

	})

}
