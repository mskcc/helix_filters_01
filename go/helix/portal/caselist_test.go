package portal

import (
    "testing"
    "strings"
    "github.com/google/go-cmp/cmp"
)


func TestCaseList(t *testing.T) {
    t.Run("Test CaseList initialization type all", func(t *testing.T) {
        ids := []string{"Sample1", "Sample2"}
        typ := CaseListTypeAll

        got := NewCaseList("pi_123", ids, typ)
        want := CaseList{
            StudyIdentifier: "pi_123",
            Category: "all_cases_in_study",
            StableId: "pi_123_all",
            Name: "All Tumors",
            Description: "All tumor samples",
            Ids: ids,
        }

        if !cmp.Equal(got, want) {
            t.Errorf("got %q is not the same as %q", got, want)
        }
    })

    t.Run("Test CaseList initialization type cnaseq", func(t *testing.T) {
        ids := []string{"Sample1", "Sample2"}
        typ := CaseListTypeCNASeq

        got := NewCaseList("pi_123", ids, typ)
        want := CaseList{
            StudyIdentifier: "pi_123",
            Category: "all_cases_with_mutation_and_cna_data",
            StableId: "pi_123_cnaseq",
            Name: "Tumors with sequencing and CNA data",
            Description: "All tumor samples that have CNA and sequencing data",
            Ids: ids,
        }

        if !cmp.Equal(got, want) {
            t.Errorf("got %q is not the same as %q", got, want)
        }
    })

    t.Run("Test CaseList initialization type cna", func(t *testing.T) {
        ids := []string{"Sample1", "Sample2"}
        typ := CaseListTypeCNA

        got := NewCaseList("pi_123", ids, typ)
        want := CaseList{
            StudyIdentifier: "pi_123",
            Category: "all_cases_with_cna_data",
            StableId: "pi_123_cna",
            Name: "Tumors CNA",
            Description: "All tumors with CNA data",
            Ids: ids,
        }

        if !cmp.Equal(got, want) {
            t.Errorf("got %q is not the same as %q", got, want)
        }
    })

    t.Run("Test CaseList initialization type seq", func(t *testing.T) {
        ids := []string{"Sample1", "Sample2"}
        typ := CaseListTypeSeq

        got := NewCaseList("pi_123", ids, typ)
        want := CaseList{
            StudyIdentifier: "pi_123",
            Category: "all_cases_with_mutation_data",
            StableId: "pi_123_sequenced",
            Name: "Sequenced Tumors",
            Description: "All sequenced tumors",
            Ids: ids,
        }

        if !cmp.Equal(got, want) {
            t.Errorf("got %q is not the same as %q", got, want)
        }
    })

    t.Run("Test add id's to the CaseList", func(t *testing.T) {
        ids := []string{"Sample1", "Sample2"}
        typ := CaseListTypeAll

        got := NewCaseList("pi_123", ids, typ)
        got.AddIds([]string{"Sample3", "Sample4"})

        want := CaseList{
            StudyIdentifier: "pi_123",
            Category: "all_cases_in_study",
            StableId: "pi_123_all",
            Name: "All Tumors",
            Description: "All tumor samples",
            Ids: []string{"Sample1", "Sample2", "Sample3", "Sample4"},
        }

        if !cmp.Equal(got, want) {
            t.Errorf("got %q is not the same as %q", got, want)
        }
    })

    t.Run("Test convert id's to a string field for output", func(t *testing.T) {
        ids := []string{"Sample1", "Sample2"}
        typ := CaseListTypeAll

        c := NewCaseList("pi_123", ids, typ)
        got := c.GetIdsString()

        want := "Sample1\tSample2"

        if !cmp.Equal(got, want) {
            t.Errorf("got %q is not the same as %q", got, want)
        }
    })

    t.Run("Test convert CaseList to a map", func(t *testing.T) {
        ids := []string{"Sample1", "Sample2"}
        typ := CaseListTypeAll
        c := NewCaseList("pi_123", ids, typ)

        got := c.ToMap()
        want := map [string]string{
            "cancer_study_identifier": "pi_123",
            "stable_id": "pi_123_all",
            "case_list_category":  "all_cases_in_study",
            "case_list_name": "All Tumors",
            "case_list_description": "All tumor samples",
            "case_list_ids": "Sample1\tSample2",
        }

        if !cmp.Equal(got, want) {
            t.Errorf("got %q is not the same as %q", got, want)
        }
    })

    t.Run("Load a case list from a map", func(t *testing.T) {
        m := map[string]string{
            "case_list_category": "all_cases_in_study",
            "stable_id": "pi_123_all",
            "case_list_name":  "All Tumors",
            "case_list_description": "All tumor samples",
            "cancer_study_identifier": "pi_123",
            "case_list_ids": "Sample1\tSample2",
        }


        got := NewCaseListFromMap(m)
        want := CaseList{
            StudyIdentifier: "pi_123",
            Category: "all_cases_in_study",
            StableId: "pi_123_all",
            Name: "All Tumors",
            Description: "All tumor samples",
            Ids: []string{"Sample1", "Sample2"},
        }

        if !cmp.Equal(got, want) {
            t.Errorf("got %q is not the same as %q", got, want)
        }
    })

    t.Run("Load a case list from a file", func(t *testing.T) {

var s string = `case_list_category: all_cases_in_study
stable_id: pi_123_all
case_list_name: All Tumors
case_list_description: All tumor samples
cancer_study_identifier: pi_123
case_list_ids: Sample1\tSample2
`
        // need to convert \t to real tabs
        var case_list_str string = strings.ReplaceAll(s,`\t`,"\t")

        reader := strings.NewReader(case_list_str)
        got := LoadCaseList(reader)
        want := CaseList{
            StudyIdentifier: "pi_123",
            Category: "all_cases_in_study",
            StableId: "pi_123_all",
            Name: "All Tumors",
            Description: "All tumor samples",
            Ids: []string{"Sample1", "Sample2"},
        }

        if !cmp.Equal(got, want) {
            t.Errorf("got %q is not the same as %q", got, want)
        }
    })

    t.Run("Create lines from a CaseList", func(t *testing.T) {
        c := CaseList{
            StudyIdentifier: "pi_123",
            Category: "all_cases_in_study",
            StableId: "pi_123_all",
            Name: "All Tumors",
            Description: "All tumor samples",
            Ids: []string{"Sample1", "Sample2"},
        }


        got := c.ToLines()
        want := []string{
            "case_list_category: all_cases_in_study",
            "stable_id: pi_123_all",
            "case_list_name: All Tumors",
            "case_list_description: All tumor samples",
            "cancer_study_identifier: pi_123",
            "case_list_ids: Sample1\tSample2",
        }

        if !cmp.Equal(got, want) {
            t.Errorf("got %q wanted %q", got, want)
        }
    })
}
