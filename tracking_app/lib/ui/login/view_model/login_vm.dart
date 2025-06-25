import 'package:flutter/material.dart';

import 'package:snacktrac/global.dart';


class LoginViewModel extends ChangeNotifier{
  String _email = '';
  String _pwd = '';

  void setEmail(String email) {
    _email = email;
  }

  void setPwd(String pwd) {
    _pwd = pwd;
  }

  Future<String?> login() async {
    try {
      final status = await authRepo.login(_email, _pwd);
      return status;
    } catch (e) {
      return e.toString();
    }
  }

  Future<String?> resetPassword() async {
    try {
      final status = await authRepo.resetPassword(_email);
      return status;
    } catch (e) {
      return e.toString();
    }
  }
  
}


