import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flex_color_scheme/flex_color_scheme.dart';

import 'package:snacktrac/ui/home_page/widgets/home_page_screen.dart';
import 'package:snacktrac/ui/profile/widgets/profile_screen.dart';
import 'package:snacktrac/ui/archive/widgets/archive_screen.dart';



class NavBar extends StatefulWidget {
  const NavBar({super.key});

  @override
  State<NavBar> createState() => _NavBarState();

}


class _NavBarState extends State<NavBar> {
  int pageIndex = 0;
  
  @override
  Widget build(BuildContext context) {
    Widget currentPage;
    switch (pageIndex) {
      case 0:
        currentPage = HomePage();
      case 1:
        currentPage = ArchivePage();
      case 2:
        currentPage = ProfilePage();
      default:
        currentPage = HomePage();
    }

    return Scaffold(
      bottomNavigationBar: NavigationBar(
        selectedIndex: pageIndex,
        onDestinationSelected: (int index) {
          setState(() {pageIndex = index;} );
        },
        destinations: [
          NavigationDestination(
            icon: Icon(Icons.auto_graph_outlined),
            selectedIcon: Icon(Icons.auto_graph),
            label: 'Summary',
          ),
          NavigationDestination(
            icon: Icon(Icons.folder_open_outlined),
            selectedIcon: Icon(Icons.folder),
            label: 'Archive',
          ),
          NavigationDestination(
            icon: Icon(Icons.face_outlined),
            selectedIcon: Icon(Icons.face),
            label: 'Profile',
          ),
        ],
      ),
      body: currentPage,
    );
  }

}






