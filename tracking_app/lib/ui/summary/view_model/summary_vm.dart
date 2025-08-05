import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import 'package:Snacked/global.dart';
import 'package:Snacked/ui/summary/widgets/prompt_screen.dart';
import 'package:Snacked/data/models/watch_data.dart';


class SummaryViewModel extends ChangeNotifier{
  Map<String, dynamic> _summaryInfo = {};
  String _comment = '';
  DateTime _summaryDate = DateTime.now().subtract(Duration(days:1));
  DateTime _updateTime = DateTime(DateTime.now().year, DateTime.now().month, DateTime.now().day, 00, 09, 00);
  DateTime? _lastShown;
  bool _addedData = false;

  DateTime get summaryDate => _summaryDate;
  bool get addedData => _addedData;

  void setAddTrue() {
    _addedData = true;
  }

  void setAddFalse() {
    _addedData = false;
  }

  void updateLastShown() {
    _lastShown = DateTime.now();
  }

  Future<bool> addData() async {
    String user = authRepo.userID;
    DateTime date = DateTime.now().subtract(Duration(days:1));
    String doc = '${date.year}${DateFormat('MMMM').format(date)}${date.day}';
    if (await fetchService.fetchData()) {
      if (await storeRepo.saveToDatabase(user, doc, fetchService.fetched)) {
      return true;
      }
    }
    return false;
  }

  Future<bool> dataCheck() async {
    String user = authRepo.userID;
    String doc = '${_summaryDate.year}${DateFormat('MMMM').format(_summaryDate)}${_summaryDate.day}';
    if (await storeRepo.getSummaries(user, doc)) {
      return true;
    }
    return false;
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
    return finalTime.difference(DateTime.now());
  }

  bool promptShown() {
    if (_lastShown == null) return false;
    return _lastShown!.year == DateTime.now().year && _lastShown!.month == DateTime.now().month
    && _lastShown!.day == DateTime.now().day;
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


