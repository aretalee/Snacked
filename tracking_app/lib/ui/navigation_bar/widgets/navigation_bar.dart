import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import 'package:Snacked/ui/navigation_bar/view_model/navigation_bar_vm.dart';


class NavBar extends StatefulWidget {
  const NavBar({super.key, required this.viewModel, required this.where, required this.child});
  final NavBarViewModel viewModel;
  final Widget child;
  final String where;

  @override
  State<NavBar> createState() => _NavBarState();
}


class _NavBarState extends State<NavBar> {

  @override
  Widget build(BuildContext context) {
    int selectedIndex;
    if (widget.where.startsWith('/home')) {
      selectedIndex = 0;
    } else if (widget.where.startsWith('/archive')) {
      selectedIndex = 1;
    } else if (widget.where.startsWith('/profile')) {
      selectedIndex = 2;
    } else { selectedIndex = 0; }

    return Scaffold(
      bottomNavigationBar: NavigationBar(
        selectedIndex: selectedIndex,
        onDestinationSelected: (int index) {
          setState(() {widget.viewModel.pageSelected(index);});
          String location = widget.viewModel.currentPage;
          context.go(location);
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
      body: widget.child,
    );
  }
}






