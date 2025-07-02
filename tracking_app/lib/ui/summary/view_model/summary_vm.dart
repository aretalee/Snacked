import 'package:flutter/material.dart';


class SummaryViewModel extends ChangeNotifier{
  bool _noData = false;
  bool _prompt = true;

  bool get noData => _noData;
  bool get prompt => _prompt;

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
  

}


