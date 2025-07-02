import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import 'package:Snacked/global.dart';


class SummaryViewModel extends ChangeNotifier{
  bool _noData = false;
  bool _prompt = true;
  DateTime _summaryDate = DateTime.now().subtract(Duration(days:1));

  bool get noData => _noData;
  bool get prompt => _prompt;
  DateTime get summaryDate => _summaryDate;

  // logic that detects if data has been imported successfully --> sets _noData to false
  // also need logic that either checks for DataTime or if data has been updated --> sets prompt to true

  void setNoDataTrue() {
    _noData = true;
  }

  void setNoDataFalse() {
    _noData = false;
  }

  void setPromptTrue() {
    _prompt = true;
  }

  void setPromptFalse() {
    _prompt = false;
  }

  Future<bool> updateComments(String comment) async {
    String docName = '${_summaryDate.year}${DateFormat('MMMM').format(_summaryDate)}${_summaryDate.day}';
    bool valid = await storeRepo.addComment(comment, authRepo.userID, docName);
    if (valid) { return true; }
    return false;
  }
  

}


