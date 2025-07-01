import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';

import 'package:Snacked/global.dart';



class AuthViewModel extends ChangeNotifier{
  bool _initialized = false;
  User? _user;

  AuthViewModel() {
    authRepo.changes.listen((u) {
      _user = u;
      _initialized = true;
      notifyListeners();
    });
  }

  bool get initialized => _initialized;
  bool get loggedIn => _user != null;
  User? get user => _user;

  
}


