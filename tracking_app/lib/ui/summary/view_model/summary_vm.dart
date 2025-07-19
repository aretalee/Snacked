import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import 'package:Snacked/global.dart';
import 'package:Snacked/ui/summary/widgets/prompt_screen.dart';


class SummaryViewModel extends ChangeNotifier{
  bool _noData = false;
  Map<String, dynamic> _summaryInfo = {};
  String _comment = '';
  DateTime _summaryDate = DateTime.now().subtract(Duration(days:1));
  DateTime _updateTime = DateTime(DateTime.now().year, DateTime.now().month, DateTime.now().day, 00, 00, 00);
  bool _promptShown = false;

  bool get noData => _noData;
  DateTime get summaryDate => _summaryDate;
  bool get promptShown => _promptShown;

  // logic that detects if data has been imported successfully --> sets _noData to false

  void setNoDataTrue() {
    _noData = true;
  }

  void setNoDataFalse() {
    _noData = false;
  }

  void setPromptTrue() {
    _promptShown = true;
  }

  Future<String> get comment async {
    if (await getComment()) { 
      if (_comment == '') { return 'You have not saved any comments'; }
      else { return _comment; }
    }
    return 'Unable to retrieve comments';
  }

  Future<bool> getComment() async {
    String docName = '${_summaryDate.year}${DateFormat('MMMM').format(_summaryDate)}${_summaryDate.day}';
    bool valid = await storeRepo.getSummaries(authRepo.userID, docName);
    if (valid) {
      _summaryInfo = storeRepo.summary;
      _comment = _summaryInfo['comments'];
      return true;
    }
    return false;
  }

  Future<bool> updateComments(String comment) async {
    String docName = '${_summaryDate.year}${DateFormat('MMMM').format(_summaryDate)}${_summaryDate.day}';
    bool valid = await storeRepo.addComment(comment, authRepo.userID, docName);
    if (valid) { return true; }
    return false;
  }

  Duration timerDuration() {
    DateTime finalTime = _updateTime;
    if (DateTime.now().isAfter(_updateTime)) {
      finalTime = finalTime.add(Duration(days:1));
    }
    if (DateTime.now().isAtSameMomentAs(_updateTime)) {
      _promptShown = false;
    }
    return finalTime.difference(DateTime.now());
  }

  Future<void> showPrompt(BuildContext context, SummaryViewModel vm) async {
    return showDialog<void> (
      context: context,
      barrierDismissible: false,
      builder: (context) {
        return PromptPage();
      }
    );
  }
  

}


