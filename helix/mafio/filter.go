package mafio

// module for holding filter criteria


// if mutation should be kept in the data_mutations_uncalled.txt instead of data_mutations.txt file
// a mutation is considered "Uncalled" if t_alt_count == 0 or is_fillout = True
// https://github.com/mskcc/pluto-cwl/issues/63
func IsUncalledFilter(mutation *Mutation) bool {
	// default value; whether mutation should be included in the data_mutations_uncalled.txt file
	keep := false

	// If fillout == True then place mutation is considered Uncalled regardless of depth
	if mutation.IsFillout {
		return true
	}

	if mutation.TAltCount < 1 {
		keep = true
	}

	return keep
}

// need to check if mutation is "uncalled", and if so, update values on the Mutation object
// For any row where t_alt_count == 0, set Mutation_Status to UNCALLED, and place in file called data_mutations_uncalled.txt
func IsUncalledMutationUpdate(mutation *Mutation) bool {
	isUncalled := IsUncalledFilter(mutation)
	if isUncalled {
		mutation.SetUncalled()
	}
	return isUncalled
}
