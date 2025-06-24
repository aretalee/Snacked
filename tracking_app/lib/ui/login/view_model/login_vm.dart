import 'package:flutter/material.dart';

import 'package:snacktrac/data/repositories/auth_repository.dart';


class LoginViewModel extends ChangeNotifier{
  final AuthRepository authRepo = AuthRepository();
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
  
}


