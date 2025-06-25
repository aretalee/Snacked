import 'package:flutter/material.dart';

import 'package:snacktrac/global.dart';



class SignUpViewModel extends ChangeNotifier{
  String _email = '';
  String _pwd = '';

  void setEmail(String email) {
    _email = email;
  }

  void setPwd(String pwd) {
    _pwd = pwd;
  }

  Future<String?> register() async {
    try {
      final status = await authRepo.register(_email, _pwd);
      return status;
    } catch (e) {
      return e.toString();
    }
  }
  
}


