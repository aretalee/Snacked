import 'package:flutter/material.dart';

import 'package:Snacked/global.dart';


class SetGoalsViewModel extends ChangeNotifier{
  Map<String, dynamic> _goalInfo = {};
  int _currentGoal = -1;
  int _desiredGoal = 0;
  String? _goalError;

  String? get goalError => _goalError;

  Future<String> get currentGoal async {
    if (await getGoal()) { 
      if (_currentGoal == -1) { return 'No custom goal set'; }
      else { return _currentGoal.toString(); }
    }
    return 'Unable to retrieve current goal';
  }

    Future<bool> getGoal() async {
    bool valid = await storeRepo.getGoal();
    if (valid) {
      _goalInfo = storeRepo.goal;
      _currentGoal = _goalInfo['targetTime'];
      return true;
    }
    return false;
  }

  void goalErrors(String goalInput) {
    final value = int.tryParse(goalInput);
    if (goalInput.isEmpty) {
      _goalError = 'Please input a goal before submitting';
    } else if (value == null) {
       _goalError = 'Please input a valid number';
    } else if (value < 0 ) {
      _goalError = 'Please input a value >= 0 ';
    } else { _goalError = null; };
  }

  bool checkGoalInput(String goalInput) {
    if (_goalError == null) {
      _desiredGoal = int.tryParse(goalInput)!;
      return true;
    }
    return false;
  }

  Future<bool> updateNewGoal() async {
    bool valid = await storeRepo.setGoal(_desiredGoal);
    if (valid) { return true; }
    return false;
  }

  

}


