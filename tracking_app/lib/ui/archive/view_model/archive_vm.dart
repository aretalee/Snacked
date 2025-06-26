import 'package:flutter/material.dart';

import 'package:snacktrac/global.dart';


class ArchiveViewModel extends ChangeNotifier{
  DateTime _dateForSummary = DateTime.now();

  DateTime get date => _dateForSummary;

  void setDate(DateTime date) {
   _dateForSummary = date;
  }

  
}


