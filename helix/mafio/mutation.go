package mafio

// definition for handling of mutation data imported from .maf format file
// https://docs.gdc.cancer.gov/Data/File_Formats/MAF_Format/

import (
	"fmt"
	"github.com/mitchellh/mapstructure"
	"os"
	"reflect"
)

// representation of Mutation object type
// TODO: implement all the default MAF fields on this struct eventually; currently just implement the ones that are needed for use cases
type Mutation struct {
	TRefCount      int64  `mapstructure:"t_ref_count"`
	TAltCount      int64  `mapstructure:"t_alt_count"`
	MutationStatus string `mapstructure:"Mutation_Status"`
	IsFillout      bool   `mapstructure:"fillout"`

	SourceMap map[string]string     // the original row from the input file
	Metadata  mapstructure.Metadata // extra info from the data import https://pkg.go.dev/github.com/mitchellh/mapstructure#Metadata
}

// convert a Mutation back to a map for use with the maf writer
func (mutation *Mutation) ToMap() map[string]string {
	// convert into a map of generic interface types
	outputMap := map[string]interface{}{}

	config := &mapstructure.DecoderConfig{
		WeaklyTypedInput: true,
		Result:           &outputMap,
	}

	decoder, err := mapstructure.NewDecoder(config)
	if err != nil {
		panic(err)
	}

	err = decoder.Decode(mutation)
	if err != nil {
		panic(err)
	}

	// remove struct fields from the map
	delete(outputMap, "SourceMap")
	delete(outputMap, "Metadata")

	// convert the map of interfaces into a map of strings
	outputMapString, err := ConvertMap(outputMap)
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed to convert: %v\n", err)
		os.Exit(1)
	}

	// add back any missing fields that were in the original SourceMap
	for sourceKey, sourceValue := range mutation.SourceMap {
		// check if a key in SourceMap is not in the outputMap
		_, present := outputMapString[sourceKey]
		if !present {
			// if not present then add the original value back in
			outputMapString[sourceKey] = sourceValue
		}
	}

	// fmt.Printf("here is the string version:\n\n%#v\n\n", outputMapString)
	return outputMapString
}


// update the Mutation for UNCALLED status
func (mutation *Mutation) SetUncalled() {
	mutation.MutationStatus = "UNCALLED"
}


// convert a map of strings into a Mutation object
func MutationFromMap(data map[string]string) Mutation {
	var mutation Mutation
	var metadata mapstructure.Metadata

	// https://pkg.go.dev/github.com/mitchellh/mapstructure#Decode
	config := &mapstructure.DecoderConfig{
		WeaklyTypedInput: true,
		Result:           &mutation,
		Metadata:         &metadata,
	}

	decoder, err := mapstructure.NewDecoder(config)
	if err != nil {
		panic(err)
	}

	err = decoder.Decode(data)
	if err != nil {
		panic(err)
	}

	mutation.SourceMap = data
	mutation.Metadata = metadata

	// fmt.Printf("\n\n%#v\n\n", mutation)

	return mutation
}

// convert a map of generic interfaces into a map of strings
func ConvertMap(m map[string]interface{}) (map[string]string, error) {
	r := make(map[string]string, len(m))

	for k, v := range m {
		switch d := v.(type) {
		case string:
			r[k] = d

		case bool:
			if d {
				r[k] = "True"
			} else {
				r[k] = "False"
			}

		case int, uint, int8, int16, int32, int64, uint8, uint16, uint32, uint64:
			r[k] = fmt.Sprintf("%d", d)

		default:
			return nil, fmt.Errorf("%s is an unsuppported type: %s", k, reflect.TypeOf(v).String())
		}
	}

	return r, nil
}
