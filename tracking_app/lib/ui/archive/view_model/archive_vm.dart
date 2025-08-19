import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:table_calendar/table_calendar.dart';

import 'package:Snacked/global.dart';


class ArchiveViewModel extends ChangeNotifier{
  DateTime _date = DateTime.now();
  Map<String, dynamic> _summaryInfo = {};
  int _eating = 0;
  int _snacking = 0;
  String _comparison = '';
  bool _compIcon = true;
  bool _noDiff = false;
  String _onTrack = '';
  bool _progressIcon = true;
  String _comments = '';

  Set<DateTime> _daysToHighlight = {};


  DateTime get date => _date;
  int get eating => _eating;
  int get snacking => _snacking;
  String get comparison => _comparison;
  String get onTrack => _onTrack;
  String get comments => _comments;
  bool get compIcon => _compIcon;
  bool get noDiff => _noDiff;
  bool get progressIcon => _progressIcon;

  Set<DateTime> get getDays => _daysToHighlight;

  void setDate(DateTime date) { _date = date; }

  Future<bool> getFromStorage() async {
    String docName = '${_date.year}${DateFormat('MMMM').format(_date)}${_date.day}';
    bool valid = await storeRepo.getSummaries(authRepo.userID, docName);
    if (valid) {
      _summaryInfo = storeRepo.summary;
      _eating = _summaryInfo['eating'];
      _snacking = _summaryInfo['snacking'];
      int? comp = _summaryInfo['comparison'];
      if (comp == null) {
        _comparison = 'No data from yesterday'; 
        _compIcon = true;
        _noDiff = true;
      } else if (comp < 0) {
        _comparison = 'Down by ${comp.abs()} min';
        _compIcon = true;
        _noDiff = false;
      } else if (comp == 0) {
        _comparison = 'No change from yesterday'; 
        _compIcon = true;
        _noDiff = true;
      } else { 
        _comparison = 'Increased by $comp min'; 
        _compIcon = false;
        _noDiff = false;
      }
      _comments = _summaryInfo['comments'];
      bool? status = _summaryInfo['onTrack'];
      if (status == null) {
        _onTrack = 'No goals set';
        _progressIcon = false;
      } else if (status) {
        _onTrack = 'You\'re on track, keep it up!';
        _progressIcon = true;
      } else { 
        _onTrack = 'No worries, let\'s try again!'; 
        _progressIcon = false;
      }
      return true;
    }
    _eating = 0;
    _snacking = 0;
    _comparison = 'No data';
    _compIcon = true;
    _noDiff = true;
    _onTrack = 'No data';
    _progressIcon = false;
    return false;
  }

  Future<void> highlightedDays() async {
    await storeRepo.fetchUserData(authRepo.userID);

    DateTime startDay = DateTime.utc(2025, 6, 22);
    while(!isSameDay(startDay, DateTime.now())) {
      setDate(startDay);
      if(await getFromStorage()) {
        _daysToHighlight.add(startDay);
      }
      startDay.add(Duration(days:1));
    }
  }
}


