package portal

import (
    "strings"
    "log"
    "io"
    "bufio"
)

var case_list_required_fields = []string{
    "case_list_category",
    "stable_id",
    "case_list_name",
    "case_list_description",
    "cancer_study_identifier",
    "case_list_ids",
}

// string label to identify different types of case lists
type CaseListType string

const (
    CaseListTypeAll CaseListType = "all"
    CaseListTypeCNASeq CaseListType = "cnaseq"
    CaseListTypeCNA CaseListType = "cna"
    CaseListTypeSeq CaseListType = "seq"
)

type CaseList struct {
    StudyIdentifier string // cancer_study_identifier studyIdentifier
    Category string // case_list_category category
    StableId string // stable_id stableID
    Name string // case_list_name name
    Description string // case_list_description description
    Ids []string // case_list_ids ids
}

// add id's to the current CaseList entry
// TODO: this should be more efficient
// try maintaining a map with ordering information instead of just a list
// https://stackoverflow.com/questions/33207197/how-can-i-create-an-array-that-contains-unique-strings
// https://stackoverflow.com/questions/34018908/golang-why-dont-we-have-a-set-datastructure
// https://stackoverflow.com/questions/18695346/how-can-i-sort-a-mapstringint-by-its-values
func (c *CaseList) AddIds(ids []string) () {
    new_ids := []string{}
    for _, v := range c.Ids {
        if ! stringInSlice(v, new_ids) {
            new_ids = append(new_ids, v)
        }
    }
    for _, v := range ids {
        if ! stringInSlice(v, new_ids) {
            new_ids = append(new_ids, v)
        }
    }
    c.Ids = new_ids
}

// get the output field string for the Ids field (case_list_ids)
func (c *CaseList) GetIdsString() string {
    var line = strings.Join(c.Ids, "\t")
    return line
}

// convert CaseList to a map with predefined keys and values for writing as output
func (c *CaseList) ToMap() map[string]string {
    var m = map[string]string{
        "cancer_study_identifier": c.StudyIdentifier,
        "stable_id": c.StableId,
        "case_list_category": c.Category,
        "case_list_name": c.Name,
        "case_list_description": c.Description,
        "case_list_ids": c.GetIdsString(),
    }
    return m
}

// convert the CaseList to a list of lines to write to the file
func (c *CaseList) ToLines() []string {
    m := c.ToMap()
    var lines = []string{}
    for _, field := range case_list_required_fields {
        var line string
        line = field + ": " + m[field]
        lines = append(lines, line)
    }
    return lines
}

// put any needed logic in here to create a new CaseList entry
func NewCaseList(studyIdentifier string, ids []string, typ CaseListType) CaseList {
    stableID := studyIdentifier
    category := "default category"
    name := "default name"
    description := "default description"

    if typ == CaseListTypeAll {
        stableID = studyIdentifier + "_all"
        category = "all_cases_in_study"
        name = "All Tumors"
        description = "All tumor samples"

    } else if typ == CaseListTypeCNASeq {
        stableID = studyIdentifier + "_cnaseq"
        category = "all_cases_with_mutation_and_cna_data"
        name = "Tumors with sequencing and CNA data"
        description = "All tumor samples that have CNA and sequencing data"

    } else if typ == CaseListTypeCNA {
        stableID = studyIdentifier + "_cna"
        category = "all_cases_with_cna_data"
        name = "Tumors CNA"
        description = "All tumors with CNA data"

    } else if typ == CaseListTypeSeq {
        stableID = studyIdentifier + "_sequenced"
        category = "all_cases_with_mutation_data"
        name = "Sequenced Tumors"
        description = "All sequenced tumors"

    } else {
        log.Fatalln("Invalid CaseListType: ", typ)
    }

    caseList := CaseList{
        StudyIdentifier: studyIdentifier,
        Category: category,
        StableId: stableID,
        Name: name,
        Description: description,
        Ids: []string{},
    }
    caseList.AddIds(ids)
    return caseList
}

// make a new case list instance from a map of values
// this is using the same keys that will be outputted
func NewCaseListFromMap(m map[string]string) CaseList {
    // make sure all keys are in the map
    for _, field := range case_list_required_fields {
        _, ok := m[field]
        if ! ok {
            log.Fatalf("Field %q not in map %q: ", field, m)
        }
    }

    studyIdentifier := m["cancer_study_identifier"]
    stableID := m["stable_id"]
    category := m["case_list_category"]
    name := m["case_list_name"]
    description := m["case_list_description"]
    ids_str := m["case_list_ids"]

    // split the tab-delimited field of sample ID's
    ids := strings.Split(ids_str, "\t")

    caseList := CaseList{
        StudyIdentifier: studyIdentifier,
        Category: category,
        StableId: stableID,
        Name: name,
        Description: description,
        Ids: ids,
    }
    return caseList
}

// load a case list from a file
func LoadCaseList(file io.Reader) CaseList {
    // load all the lines from the file
    // need to initialize a buffer for the scanner that is larger than the default 64KB size
    // this could be really large if there are a ton of sample ID's
    const maxCapacity = 2048*1024*10 // 20Mb
    buf := make([]byte, maxCapacity)

    scanner := bufio.NewScanner(file)
    scanner.Buffer(buf, maxCapacity)

    var lines []string

    for scanner.Scan() {
        var line string
        line = scanner.Text()
        lines = append(lines, line)
    }
    if err := scanner.Err(); err != nil {
        log.Fatal(err)
    }

    // convert the lines into a map
    m := make(map[string]string)

    for _, line := range lines {
        fields := strings.Split(line, ":")
        key := fields[0]
        value := fields [1]
        // trim leading and trailing spaces
        key = strings.TrimSpace(key)
        value = strings.TrimSpace(value)
        // add to map
        m[key] = value
    }

    // convert map into a CaseList
    c := NewCaseListFromMap(m)

    return c
}

// function for checking if a string is in a slice
// because we cannot use slices.Contains because we cannot use Go 1.18 because macOS is old
// https://stackoverflow.com/questions/15323767/does-go-have-if-x-in-construct-similar-to-python
func stringInSlice(a string, list []string) bool {
    for _, b := range list {
        if b == a {
            return true
        }
    }
    return false
}
