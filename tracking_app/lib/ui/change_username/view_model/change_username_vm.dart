import 'package:flutter/material.dart';

import 'package:Snacked/global.dart';


class ChangeNameViewModel extends ChangeNotifier{
  String _name = '';
  String? _nameError;

  void setNewName(String name) {
    _name = name;
  }

  String? get nameError => _nameError;

  String? getName() { return _name; }

  Future<String?> changeUsername() async {
    try {
      final status = await authRepo.changeUsername(_name);
      return status;
    } catch (e) {
      return e.toString();
    }
  }

  void nameErrors(String nameInput) {
    if (nameInput.isEmpty) {
      _nameError = 'Please enter an email address';
    }
  }

  bool nameCheck(String nameInput) {
    if (_nameError == null) {
      setNewName(nameInput);
      return true;
    }
    return false;
  }

  bool nameSuccess(String? status) {
    if (status != null && status.contains('Success')) {
      return true;
    }
    return false;
  }
}

