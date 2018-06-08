
import unittest

import blendomaticutil


class TestUtils(unittest.TestCase):

    def test_input_parser(self):
        input_objects = "[obj1, obj2]"
        obj_list = blendomaticutil.parse_list_string(input_objects)
        self.assertEqual(obj_list, [["obj1", "obj2"]])

        input_objects = "obj1, obj2"
        obj_list = blendomaticutil.parse_list_string(input_objects)
        self.assertEqual(obj_list, [["obj1"], ["obj2"]])

        # does combined also work ?
        input_objects = "obj1, obj2, [       obj3 , obj4 ]"
        obj_list = blendomaticutil.parse_list_string(input_objects)
        self.assertEqual(obj_list, [["obj1"], ["obj2"], ["obj3", "obj4"]])


    def test_input_output_mapping(self):
        input_objects = "[obj1, obj2]"
        output_files = "out.obj"

        combined = blendomaticutil.map_inputs_to_ouputs(
            input_objects, output_files)

        self.assertEqual(len(combined), 1)
        first_inputs = combined[0][0]
        self.assertEqual("obj1", first_inputs[0])
        self.assertEqual("obj2", first_inputs[1])

        first_outputs = combined[0][1]
        self.assertEqual(len(first_outputs), 1)
        self.assertEqual("out.obj", first_outputs[0])

    def test_input_output_mapping_non_list_syntax(self):
        input_objects = "obj1, obj2"
        output_files = "out1.obj, out2.obj"

        combined = blendomaticutil.map_inputs_to_ouputs(
            input_objects, output_files)

        self.assertEqual(len(combined), 2)
        first_inputs = combined[0][0]
        self.assertEqual("obj1", first_inputs[0])

        first_outputs = combined[0][1]
        self.assertEqual(len(first_outputs), 1)
        self.assertEqual("out1.obj", first_outputs[0])

        first_inputs = combined[1][0]
        self.assertEqual("obj2", first_inputs[0])

        first_outputs = combined[1][1]
        self.assertEqual(len(first_outputs), 1)
        self.assertEqual("out2.obj", first_outputs[0])

    def test_input_output_mapping_multiple_inputs(self):
        input_objects = "[obj1, obj2], [obj3]"
        some_options = "[23], [24]"
        output_files = "[out1.obj], [out2.obj]"

        out_lists = blendomaticutil.map_inputs_to_ouputs(
            input_objects, some_options, output_files)

        self.assertEqual(len(out_lists), 2)
        first_inputs = out_lists[0]
        self.assertEqual("obj1", first_inputs[0][0])
        self.assertEqual("obj2", first_inputs[0][1])
        first_inputs = out_lists[1]
        self.assertEqual("24", first_inputs[1][0])

    def test_input_output_mapping_interpolate(self):
        input_objects = "[obj1, obj2], [obj3]"
        some_options = "23"
        output_files = "[out1.obj], [out2.obj]"

        out_lists = blendomaticutil.map_inputs_to_ouputs(
            input_objects, some_options, output_files)

        first_inputs = out_lists[0]
        # should have been extrapolated, test for it
        self.assertEqual("23", first_inputs[1][0])
        first_inputs = out_lists[1]
        self.assertEqual("23", first_inputs[1][0])
