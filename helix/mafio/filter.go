package mafio

// if mutation should be kept in the data_mutations_uncalled.txt instead of data_mutations.txt file
// a mutation is considered "Uncalled" if t_alt_count == 0 or is_fillout = True
// https://github.com/mskcc/pluto-cwl/issues/63
func IsUncalledFilter(mutation Mutation) bool {
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
