import 'package:flutter/material.dart';


class NavBarViewModel extends ChangeNotifier{
  int pageIndex = 0;

  String get currentPage{
    switch (pageIndex) {
      case 0:
        return '/summary';
      case 1:
       return '/archive';
      case 2:
        return '/profile';
      default:
        return '/summary';
    }
  }

  void pageSelected(int index) {
    pageIndex = index;
    notifyListeners();
  }
}

