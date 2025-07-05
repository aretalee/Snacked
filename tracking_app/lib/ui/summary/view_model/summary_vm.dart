import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import 'package:Snacked/global.dart';
import 'package:Snacked/ui/summary/widgets/prompt_screen.dart';


class SummaryViewModel extends ChangeNotifier{
  bool _noData = false;
  DateTime _summaryDate = DateTime.now().subtract(Duration(days:1));
  DateTime _updateTime = DateTime(DateTime.now().year, DateTime.now().month, DateTime.now().day, 00, 00, 00);

  bool get noData => _noData;
  DateTime get summaryDate => _summaryDate;

  // logic that detects if data has been imported successfully --> sets _noData to false

  void setNoDataTrue() {
    _noData = true;
  }

  void setNoDataFalse() {
    _noData = false;
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
    return finalTime.difference(DateTime.now());
  }

  Future<void> showPrompt(BuildContext context) async {
    return showDialog<void> (
      context: context,
      barrierDismissible: false,
      builder: (context) {
        return PromptPage();
      }
    );
  }
  

}


