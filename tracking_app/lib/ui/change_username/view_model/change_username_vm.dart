import 'package:flutter/material.dart';

import 'package:snacktrac/global.dart';


class ChangeNameViewModel extends ChangeNotifier{
  String _name = '';

  void setNewName(String name) {
    _name = name;
  }

  String? getName() { return _name; }

  Future<String?> changeUsername() async {
    try {
      final status = await authRepo.changeUserame(_name);
      return status;
    } catch (e) {
      return e.toString();
    }
  }
  
}

