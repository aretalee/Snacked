import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import 'package:snacktrac/global.dart';


class ArchiveViewModel extends ChangeNotifier{
  DateTime _date = DateTime.now();
  Map<String, dynamic> _summaryInfo = {};
  String _errorMessage = '';
  int _eating = 0;
  int _snacking = 0;
  String _comparison = '';
  String _onTrack = '';
  String _comments = '';

  DateTime get date => _date;
  Map<String, dynamic> get summaryInfo => _summaryInfo;
  String get errorMessage => _errorMessage;
  int get eating => _eating;
  int get snacking => _snacking;
  String get comparison => _comparison;
  String get onTrack => _onTrack;
  String get comments => _comments;

  void setDate(DateTime date) {
   _date = date;
  }

  // bool getFromStorage() {
  //   String docName = '${_date.year}${DateFormat('MMMM').format(_date)}${_date.day}';
  //   bool valid = storeRepo.getDocument(docName);
  //   if (valid) {
  //     _summaryInfo = storeRepo.contents;
  //     _eating = _summaryInfo['eating'];
  //     _snacking = _summaryInfo['snacking'];
  //     int comp = _summaryInfo['comparison'];
  //     if (comp < 0) {
  //       _comparison = 'Down by ${comp.abs()} min';
  //     } else { _comparison = 'Increased by ${comp} min'; }
  //     _comments = _summaryInfo['comments'];
  //     bool status = _summaryInfo['onTrack'];
  //     if (status) {
  //       _onTrack = 'You\'re on track, keep it up!';
  //     } else { _onTrack = 'No worries, try again tomorrow!'; }
  //     return true;
  //   } else { _errorMessage = storeRepo.error; }
  //   return false;
  // }

    Future<bool> getFromStorage() async {
    String docName = '${_date.year}${DateFormat('MMMM').format(_date)}${_date.day}';
    bool valid = await storeRepo.getDocument(docName);
    if (valid) {
      _summaryInfo = storeRepo.contents;
      _eating = _summaryInfo['eating'];
      _snacking = _summaryInfo['snacking'];
      int comp = _summaryInfo['comparison'];
      if (comp < 0) {
        _comparison = 'Down by ${comp.abs()} min';
      } else { _comparison = 'Increased by ${comp} min'; }
      _comments = _summaryInfo['comments'];
      bool status = _summaryInfo['onTrack'];
      if (status) {
        _onTrack = 'You\'re on track, keep it up!';
      } else { _onTrack = 'No worries, try again tomorrow!'; }
      return true;
    } else { _errorMessage = storeRepo.error; }
    return false;
  }

  
}


