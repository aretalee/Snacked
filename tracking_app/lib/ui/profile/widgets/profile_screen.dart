import 'package:flutter/material.dart';

import 'package:snacktrac/ui/set_goals/widgets/set_goals_screen.dart';
import 'package:snacktrac/ui/export_data/widgets/export_screen.dart';
import 'package:snacktrac/ui/change_password/widgets/change_password_screen.dart';
import 'package:snacktrac/ui/info/widgets/info_screen.dart';


class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context) {

    return Scaffold (
      appBar: AppBar(backgroundColor: Colors.black),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            CircleAvatar(
              radius:50,
              backgroundColor: Colors.white,
              child: CircleAvatar(
                radius:45,
                child: Icon(Icons.person_2_outlined, color: Colors.white, size: 50,)
              )
            ),
            const SizedBox(height:15),
            Text('User 1908', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
            const SizedBox(height:45),
            FilledButton(
              onPressed: () {
                Navigator.push(
                  context, MaterialPageRoute(builder: (context) => const SetGoalsPage()),
                );
              }, 
              child: const Text('Set Daily Goal'), 
            ),
            const SizedBox(height:15),
            FilledButton(
              onPressed: () {
                Navigator.push(
                  context, MaterialPageRoute(builder: (context) => const ExportPage()),
                );
              }, 
              child: const Text('Export Data'),
            ),
            const SizedBox(height:15),
            FilledButton(
              onPressed: () {
                Navigator.push(
                  context, MaterialPageRoute(builder: (context) => const ChangePasswordPage()),
                );
              }, 
              child: const Text('Change Password'),
            ),
            const SizedBox(height:15),
            FilledButton(
              onPressed: () {
                Navigator.push(
                  context, MaterialPageRoute(builder: (context) => const InfoPage()),
                );
              }, 
              child: const Text('About SnackTrac'),
            ),
          ],
        )
      )
    );
  }

}