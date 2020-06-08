#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit tests for the generate_cbioPortal_file.cwl file
"""
import os
import json
import unittest
from tempfile import TemporaryDirectory, NamedTemporaryFile


# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .tools import run_command
    from .settings import CWL_DIR, CWL_ARGS, DATA_SETS #ARGOS_VERSION_STRING, IS_IMPACT, PORTAL_FILE, PORTAL_CNA_FILE

if __name__ == "__main__":
    from tools import run_command
    from settings import CWL_DIR, CWL_ARGS, DATA_SETS #ARGOS_VERSION_STRING, IS_IMPACT, PORTAL_FILE, PORTAL_CNA_FILE

cwl_file = os.path.join(CWL_DIR, 'generate_cBioPortal_file.cwl')

class TestGenerateCbioFilesCWL(unittest.TestCase):
    def test_generate_meta_sample(self):
        """
        meta_clinical_sample.txt
        """
        input_json = {
        "subcommand": "meta_sample",
        "cancer_study_id": "cancer_study",
        "sample_data_filename": "data_clinical_sample.txt",
        "output_filename": "meta_clinical_sample.txt"
        }
        with TemporaryDirectory() as tmpdir:
            input_json_file = os.path.join(tmpdir, "input.json")
            with open(input_json_file, "w") as json_out:
                json.dump(input_json, json_out)

            output_dir = os.path.join(tmpdir, "output")
            tmp_dir = os.path.join(tmpdir, "tmp")
            cache_dir = os.path.join(tmpdir, "cache")

            command = [
                "cwl-runner",
                *CWL_ARGS,
                "--outdir", output_dir,
                "--tmpdir-prefix", tmp_dir,
                "--cachedir", cache_dir,
                cwl_file, input_json_file
                ]
            returncode, proc_stdout, proc_stderr = run_command(command)

            if returncode != 0:
                print(proc_stderr)

            self.assertEqual(returncode, 0)

            output_json = json.loads(proc_stdout)

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, "meta_clinical_sample.txt"),
                    'basename': "meta_clinical_sample.txt",
                    'class': 'File',
                    'checksum': 'sha1$14021d16e19aa53440f953aece0e66e41d09c7f5',
                    'size': 140,
                    'path': os.path.join(output_dir, "meta_clinical_sample.txt")
                    }
                }
            self.maxDiff = None
            self.assertDictEqual(output_json, expected_output)

    def test_generate_data_clinical_patient(self):
        """
        data_clinical_patient.txt

        generate_cbioPortal_files.py \
        patient \
        --data-clinical-file "$(DATA_CLINICAL_FILE)" \
        --output "$(CBIO_CLINCIAL_PATIENT_DATA_FILE)"
        """
        data_clinical_file = os.path.join(DATA_SETS['Proj_08390_G']['INPUTS_DIR'], "Proj_08390_G_sample_data_clinical.txt")

        input_json = {
        "subcommand": "patient",
        "data_clinical_file": {
            "path": data_clinical_file,
            "class": "File"
            },
        "output_filename": "data_clinical_patient.txt"
        }
        with TemporaryDirectory() as tmpdir:
            input_json_file = os.path.join(tmpdir, "input.json")
            with open(input_json_file, "w") as json_out:
                json.dump(input_json, json_out)

            output_dir = os.path.join(tmpdir, "output")
            tmp_dir = os.path.join(tmpdir, "tmp")
            cache_dir = os.path.join(tmpdir, "cache")

            command = [
                "cwl-runner",
                *CWL_ARGS,
                "--outdir", output_dir,
                "--tmpdir-prefix", tmp_dir,
                "--cachedir", cache_dir,
                cwl_file, input_json_file
                ]
            returncode, proc_stdout, proc_stderr = run_command(command)

            if returncode != 0:
                print(proc_stderr)

            self.assertEqual(returncode, 0)

            output_json = json.loads(proc_stdout)

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, 'data_clinical_patient.txt'),
                    'basename': 'data_clinical_patient.txt',
                    'class': 'File',
                    'checksum': 'sha1$9417dcabddd6ab2cbe98167bccd9b9e4fa182562',
                    'size': 643,
                    'path': os.path.join(output_dir,'data_clinical_patient.txt')
                }
            }
            self.maxDiff = None
            self.assertDictEqual(output_json, expected_output)

    def test_generate_data_clinical_sample(self):
        """
        # data_clinical_sample.txt

        generate_cbioPortal_files.py \
        sample \
        --data-clinical-file "$(DATA_CLINICAL_FILE)" \
        --sample-summary-file "$(SAMPLE_SUMMARY_FILE)" \
        --project-pi "$(PROJ_PI)" \
        --request-pi "$(REQUEST_PI)" \
        --output "$(CBIO_CLINICAL_SAMPLE_DATA_FILE)"
        """
        data_clinical_file = os.path.join(DATA_SETS['Proj_08390_G']['INPUTS_DIR'], "Proj_08390_G_sample_data_clinical.txt")
        sample_summary_file = os.path.join(DATA_SETS['Proj_08390_G']['QC_DIR'], "Proj_08390_G_SampleSummary.txt")

        input_json = {
        "subcommand": "sample",
        "data_clinical_file": {
            "path": data_clinical_file,
            "class": "File"
            },
        "sample_summary_file": {
            "path": sample_summary_file,
            "class": "File"
            },
        "output_filename": "data_clinical_sample.txt",
        "project_pi": "Dr. Jones",
        "request_pi": "Dr. Franklin"
        }

        with TemporaryDirectory() as tmpdir:
            input_json_file = os.path.join(tmpdir, "input.json")
            with open(input_json_file, "w") as json_out:
                json.dump(input_json, json_out)

            output_dir = os.path.join(tmpdir, "output")
            tmp_dir = os.path.join(tmpdir, "tmp")
            cache_dir = os.path.join(tmpdir, "cache")

            command = [
                "cwl-runner",
                *CWL_ARGS,
                "--outdir", output_dir,
                "--tmpdir-prefix", tmp_dir,
                "--cachedir", cache_dir,
                cwl_file, input_json_file
                ]
            returncode, proc_stdout, proc_stderr = run_command(command)

            if returncode != 0:
                print(proc_stderr)

            self.assertEqual(returncode, 0)

            output_json = json.loads(proc_stdout)

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, 'data_clinical_sample.txt'),
                    'basename': 'data_clinical_sample.txt',
                    'class': 'File',
                    'checksum': 'sha1$2a0c59593fa7726743b2fe46db9d955dbc625453',
                    'size': 7592,
                    'path': os.path.join(output_dir,'data_clinical_sample.txt')
                }
            }
            self.maxDiff = None
            self.assertDictEqual(output_json, expected_output)

    def test_generate_meta_study(self):
        """
        # meta_study.txt
            generate_cbioPortal_files.py \
            study \
            --cancer-study-id "$(PROJ_ID)" \
            --name "$(PROJ_NAME)" \
            --short-name "$(PROJ_SHORT_NAME)" \
            --type-of-cancer "$(CANCER_TYPE)" \
            --description "$(PROJ_DESC)" \
            --output "$(CBIO_META_STUDY_FILE)" \
            $(EXTRA_GROUPS_STR)
        """
        input_json = {
        "subcommand": "study",
        "output_filename": "meta_study.txt",
        "cancer_study_id": "cancer_study",
        "name": "cancer_study",
        "short_name": "cancer_study",
        "type_of_cancer": "MEL",
        "description": "description",
        "extra_groups": "FOO1"
        }
        with TemporaryDirectory() as tmpdir:
            input_json_file = os.path.join(tmpdir, "input.json")
            with open(input_json_file, "w") as json_out:
                json.dump(input_json, json_out)

            output_dir = os.path.join(tmpdir, "output")
            tmp_dir = os.path.join(tmpdir, "tmp")
            cache_dir = os.path.join(tmpdir, "cache")

            command = [
                "cwl-runner",
                *CWL_ARGS,
                "--outdir", output_dir,
                "--tmpdir-prefix", tmp_dir,
                "--cachedir", cache_dir,
                cwl_file, input_json_file
                ]
            returncode, proc_stdout, proc_stderr = run_command(command)

            if returncode != 0:
                print(proc_stderr)

            self.assertEqual(returncode, 0)

            output_json = json.loads(proc_stdout)

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, 'meta_study.txt'),
                    'basename': 'meta_study.txt',
                    'class': 'File',
                    'checksum': 'sha1$9625b915f0eba999305026833fa8b32b6ebebaa0',
                    'size': 161,
                    'path': os.path.join(output_dir,'meta_study.txt')
                }
            }
            self.maxDiff = None
            self.assertDictEqual(output_json, expected_output)

    def test_meta_clinical_patient(self):
        """
        # meta_clinical_patient.txt
        generate_cbioPortal_files.py \
        meta_patient \
        --cancer-study-id "$(PROJ_ID)" \
        --patient-data-filename "$(CBIO_CLINCIAL_PATIENT_DATA_FILENAME)" \
        --output "$(CBIO_CLINCAL_PATIENT_META_FILE)"
        """
        input_json = {
        "subcommand": "meta_patient",
        "output_filename": "meta_clinical_patient.txt",
        "cancer_study_id": "cancer_study",
        "patient_data_filename": "data_clinical_patient.txt"
        }
        with TemporaryDirectory() as tmpdir:
            input_json_file = os.path.join(tmpdir, "input.json")
            with open(input_json_file, "w") as json_out:
                json.dump(input_json, json_out)

            output_dir = os.path.join(tmpdir, "output")
            tmp_dir = os.path.join(tmpdir, "tmp")
            cache_dir = os.path.join(tmpdir, "cache")

            command = [
                "cwl-runner",
                *CWL_ARGS,
                "--outdir", output_dir,
                "--tmpdir-prefix", tmp_dir,
                "--cachedir", cache_dir,
                cwl_file, input_json_file
                ]
            returncode, proc_stdout, proc_stderr = run_command(command)

            if returncode != 0:
                print(proc_stderr)

            self.assertEqual(returncode, 0)

            output_json = json.loads(proc_stdout)

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, 'meta_clinical_patient.txt'),
                    'basename': 'meta_clinical_patient.txt',
                    'class': 'File',
                    'checksum': 'sha1$cae62ab4638ff2ff39b71a43b5bd996f8eea16ea',
                    'size': 142,
                    'path': os.path.join(output_dir,'meta_clinical_patient.txt')
                }
            }
            self.maxDiff = None
            self.assertDictEqual(output_json, expected_output)

    def test_generate_meta_CNA(self):
        """
        # meta_CNA.txt
            generate_cbioPortal_files.py \
            meta_cna \
            --cancer-study-id "$(PROJ_ID)" \
            --cna-data-filename "$(CBIO_CNA_DATA_FILENAME)" \
            --output "$(CBIO_META_CNA_FILE)"
        """
        input_json = {
        "subcommand": "meta_cna",
        "output_filename": "meta_CNA.txt",
        "cancer_study_id": "cancer_study",
        "cna_data_filename": "data_CNA.txt"
        }
        with TemporaryDirectory() as tmpdir:
            input_json_file = os.path.join(tmpdir, "input.json")
            with open(input_json_file, "w") as json_out:
                json.dump(input_json, json_out)

            output_dir = os.path.join(tmpdir, "output")
            tmp_dir = os.path.join(tmpdir, "tmp")
            cache_dir = os.path.join(tmpdir, "cache")

            command = [
                "cwl-runner",
                *CWL_ARGS,
                "--outdir", output_dir,
                "--tmpdir-prefix", tmp_dir,
                "--cachedir", cache_dir,
                cwl_file, input_json_file
                ]
            returncode, proc_stdout, proc_stderr = run_command(command)

            if returncode != 0:
                print(proc_stderr)

            self.assertEqual(returncode, 0)

            output_json = json.loads(proc_stdout)

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, 'meta_CNA.txt'),
                    'basename': 'meta_CNA.txt',
                    'class': 'File',
                    'checksum': 'sha1$a0c50ba21af32710c6895201ec2ec74809f43fec',
                    'size': 270,
                    'path': os.path.join(output_dir,'meta_CNA.txt')
                }
            }
            self.maxDiff = None
            self.assertDictEqual(output_json, expected_output)

    def test_generate_meta_fusion(self):
        """
        # meta_fusions.txt

        generate_cbioPortal_files.py \
        meta_fusion \
        --cancer-study-id "$(PROJ_ID)" \
        --fusion-data-filename "$(CBIO_FUSION_DATA_FILENAME)" \
        --output "$(CBIO_META_FUSIONS_FILE)"
        """
        input_json = {
        "subcommand": "meta_fusion",
        "output_filename": "meta_fusions.txt",
        "cancer_study_id": "cancer_study",
        "fusion_data_filename": "data_fusions.txt"
        }
        with TemporaryDirectory() as tmpdir:
            input_json_file = os.path.join(tmpdir, "input.json")
            with open(input_json_file, "w") as json_out:
                json.dump(input_json, json_out)

            output_dir = os.path.join(tmpdir, "output")
            tmp_dir = os.path.join(tmpdir, "tmp")
            cache_dir = os.path.join(tmpdir, "cache")

            command = [
                "cwl-runner",
                *CWL_ARGS,
                "--outdir", output_dir,
                "--tmpdir-prefix", tmp_dir,
                "--cachedir", cache_dir,
                cwl_file, input_json_file
                ]
            returncode, proc_stdout, proc_stderr = run_command(command)

            if returncode != 0:
                print(proc_stderr)

            self.assertEqual(returncode, 0)

            output_json = json.loads(proc_stdout)

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, 'meta_fusions.txt'),
                    'basename': 'meta_fusions.txt',
                    'class': 'File',
                    'checksum': 'sha1$5e71daac57615260e685b9f7184a86ddf0e3a6d4',
                    'size': 227,
                    'path': os.path.join(output_dir,'meta_fusions.txt')
                }
            }
            self.maxDiff = None
            self.assertDictEqual(output_json, expected_output)

    def test_generate_meta_mutations_extended(self):
        """
        # meta_mutations_extended.txt

        generate_cbioPortal_files.py \
        meta_mutations \
        --cancer-study-id "$(PROJ_ID)" \
        --mutations-data-filename "$(CBIO_MUTATION_DATA_FILENAME)" \
        --output "$(CBIO_META_MUTATIONS_FILE)"
        """
        input_json = {
        "subcommand": "meta_mutations",
        "output_filename": "meta_mutations_extended.txt",
        "cancer_study_id": "cancer_study",
        "mutations_data_filename": "data_mutations_extended.txt"
        }
        with TemporaryDirectory() as tmpdir:
            input_json_file = os.path.join(tmpdir, "input.json")
            with open(input_json_file, "w") as json_out:
                json.dump(input_json, json_out)

            output_dir = os.path.join(tmpdir, "output")
            tmp_dir = os.path.join(tmpdir, "tmp")
            cache_dir = os.path.join(tmpdir, "cache")

            command = [
                "cwl-runner",
                *CWL_ARGS,
                "--outdir", output_dir,
                "--tmpdir-prefix", tmp_dir,
                "--cachedir", cache_dir,
                cwl_file, input_json_file
                ]
            returncode, proc_stdout, proc_stderr = run_command(command)

            if returncode != 0:
                print(proc_stderr)

            self.assertEqual(returncode, 0)

            output_json = json.loads(proc_stdout)

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, 'meta_mutations_extended.txt'),
                    'basename': 'meta_mutations_extended.txt',
                    'class': 'File',
                    'checksum': 'sha1$d6681566b68ec2eba1c16369f6838ed52986b044',
                    'size': 253,
                    'path': os.path.join(output_dir,'meta_mutations_extended.txt')
                }
            }
            self.maxDiff = None
            self.assertDictEqual(output_json, expected_output)


if __name__ == "__main__":
    unittest.main()
