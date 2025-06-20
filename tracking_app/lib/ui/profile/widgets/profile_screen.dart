import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:go_router/go_router.dart';
import 'package:flex_color_scheme/flex_color_scheme.dart';


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
              onPressed: () {}, 
              // style: FilledButton.styleFrom(
              //   backgroundColor: const Color(0x8405BE),
              // ),
              child: const Text('Set Daily Goal'), 
            ),
            const SizedBox(height:15),
            FilledButton(
              onPressed: () {}, 
              child: const Text('Export Data'),
            ),
            const SizedBox(height:15),
            FilledButton(
              onPressed: () {}, 
              child: const Text('Change Password'),
            ),
            const SizedBox(height:15),
            FilledButton(
              onPressed: () {}, 
              child: const Text('About SnackTrac'),
            ),
          ],
        )
      )
    );
  }

}