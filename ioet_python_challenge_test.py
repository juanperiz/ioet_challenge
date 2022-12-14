#!/usr/bin/env python
import unittest
import ioet_python_challenge as ioet

class TestIOETScript(unittest.TestCase):
 
 def test_missing_input_file(self):
  self.assertRaises(SystemExit, ioet.read_input_file, 'file_no_exists.txt')
 
 def test_no_data_in_input_file(self):
  self.assertRaises(SystemExit, ioet.get_data_from_input_file, '')
 
 def test_no_good_format_at_all_in_input_file_1(self):
  self.assertRaises(SystemExit, ioet.get_data_from_input_file, ['RENE='])
 
 def test_no_good_format_at_all_in_input_file_2(self):
  self.assertRaises(SystemExit, ioet.get_data_from_input_file, ['RENE=MO'])

 def test_no_good_format_at_all_in_input_file_3(self):
  self.assertRaises(SystemExit, ioet.get_data_from_input_file, ['=MO10:00-21:00'])
 
 def test_no_good_format_at_all_in_input_file_4(self):
  self.assertRaises(SystemExit, ioet.get_data_from_input_file, ['RENE=MO10:00-21:00KIM=MO10:00-21:00,'])

 def test_no_good_format_at_all_in_input_file_5(self):
  self.assertRaises(SystemExit, ioet.get_data_from_input_file, ['RENE=MO10:00-KIM=MO10:00-21:00,'])
 
 def test_good_raw_record(self):
  actual = ioet.get_data_from_input_file(['RENE=MO10:00-12:00,WE10:00-12:00,FR10:00-12:00'])
  expected = {'RENE': ['MO10:00-12:00', 'WE10:00-12:00', 'FR10:00-12:00']}
  self.assertEqual(expected, actual)

 def test_good_raw_records_with_two_employee_records(self):
  actual = ioet.get_data_from_input_file(['RENE=MO10:00-12:00,WE10:00-12:00','KIM=FR10:00-12:00'])
  expected = {'RENE': ['MO10:00-12:00', 'WE10:00-12:00'], 'KIM':['FR10:00-12:00']}
  self.assertEqual(expected, actual)

 def test_good_raw_record_with_future_skipped_record(self):
  actual = ioet.get_data_from_input_file(['RENE=MO10:00-12:00,WE10:00-12:00FR10:00-12:00','KIM=FR10:00-12:00'])
  expected = {'RENE': ['MO10:00-12:00', 'WE10:00-12:00FR10:00-12:00'], 'KIM':['FR10:00-12:00']}
  self.assertEqual(expected, actual)

 def test_duplicated_and_overlapping_hours_in_differents_raw_record(self):
  actual = ioet.get_data_from_input_file(['RENE=MO10:00-12:00,WE10:00-12:00,FR10:00-12:00', 'RENE=MO10:00-12:00,WE10:00-12:00,FR10:00-12:00'])
  expected = {'RENE': ['MO10:00-12:00', 'WE10:00-12:00', 'FR10:00-12:00']}
  self.assertEqual(expected, actual)

 def test_check_coherent_record_time(self):
  actual = ioet.record_time_interval_is_coherent(1000,1300)
  expected = True
  self.assertEqual(expected, actual)

 def test_check_incoherent_record_time(self):
  self.assertRaises(Exception, ioet.record_time_interval_is_coherent, 1400, 1300)
 
 def test_check_coherent_record_time(self):
  actual = ioet.record_time_interval_is_coherent(1000,1300)
  expected = True
  self.assertEqual(expected, actual)

 def test_check_monday_first_day_of_week(self):
  actual = ioet.get_number_of_day('MO')
  expected = 1
  self.assertEqual(expected, actual)

 def test_check_sunday_last_day_of_week(self):
  actual = ioet.get_number_of_day('SU')
  expected = 7
  self.assertEqual(expected, actual)

 def test_adjust_0000_to_2400(self):
  actual = ioet.adjust_0000_to_2400(0,0)
  expected = 24
  self.assertEqual(expected, actual)

 def test_no_need_to_adjust_0000_to_24000(self):
  actual = ioet.adjust_0000_to_2400(23,0)
  expected = 23
  self.assertEqual(expected, actual)

 def test_discrete_time_to_planar_time(self):
  actual = ioet.time_to_planar_time("09:00")
  expected = 540
  self.assertEqual(expected, actual)

 def test_discrete_time_to_planar_time_0000_to_2400_case(self):
  actual = ioet.time_to_planar_time("00:00")
  expected = 1440
  self.assertEqual(expected, actual)

 def test_discrete_time_to_planar_time_0001_case(self):
  actual = ioet.time_to_planar_time("00:01")
  expected = 1
  self.assertEqual(expected, actual)

 def test_get_basic_hourly_payment_hour_inside_timeshift(self):
  actual = ioet.get_hourly_payment('MO','10:00','12:00')
  expected = 30
  self.assertEqual(expected, actual)

 def test_early_morning_basic_wage_on_monday(self):
  actual = ioet.calculate_basic_wage(1,0,60)
  expected = 25
  self.assertEqual(expected, actual)

 def test_early_morning_basic_wage_on_sunday(self):
  actual = ioet.calculate_basic_wage(7,0,60)
  expected = 30
  self.assertEqual(expected, actual)

 def test_early_morning_on_sunday_one_interval_non_recursive(self):
  actual = ioet.calculate_hourly_amount(7,0,60)
  expected = 30
  self.assertEqual(expected, actual)

 def test_early_morning_on_sunday_two_intervals_recursive(self):
  actual = round(ioet.calculate_hourly_amount(7,0,600),2)
  expected = 289.67
  self.assertEqual(expected, actual)

 def test_good_normal_specific_employee_paycheck_case_RENE(self):
  actual = round(ioet.get_weekly_payment_for_specific_employee( ['MO10:00-12:00', 'TU10:00-12:00', 'TH01:00-03:00','SA14:00-18:00', 'SU20:00-21:00' ]),2)
  expected = 215
  self.assertEqual(expected, actual)

 def test_good_normal_specific_employee_paycheck_case_ASTRID(self):
  actual = round(ioet.get_weekly_payment_for_specific_employee( ['MO10:00-12:00', 'TH12:00-14:00', 'SU20:00-21:00' ]),2)
  expected = 85
  self.assertEqual(expected, actual)

 def test_check_incoherent_hours_input(self):
  self.assertRaises(Exception, ioet.get_hour_and_minutes_from_time_string, "27:30")
 
 def test_check_incoherent_minutes_input(self):
  self.assertRaises(Exception, ioet.get_hour_and_minutes_from_time_string, "07:69")

 def test_check_coherent_hours_and_minutes_input(self):
  actual = ioet.get_hour_and_minutes_from_time_string("21:35")
  expected = (21,35)
  self.assertEqual(expected, actual)

if __name__ == '__main__':
 unittest.main()