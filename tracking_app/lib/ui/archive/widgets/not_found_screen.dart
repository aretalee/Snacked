import 'package:flutter/material.dart';

import 'package:snacktrac/ui/archive/view_model/archive_vm.dart';

class NotFoundPage extends StatefulWidget {
  const NotFoundPage({super.key, required this.viewModel});
  final ArchiveViewModel viewModel;

  @override
  State<NotFoundPage> createState() =>  _NotFoundPageState();
}


class _NotFoundPageState extends State<NotFoundPage> {

  @override
  Widget build(BuildContext context) {

    return Scaffold (
      appBar: AppBar(backgroundColor: Colors.black),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Center(
          child: Card(
            child: Padding(
              padding: const EdgeInsets.all(30.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                mainAxisSize: MainAxisSize.min,
                children: [
                  const SizedBox(height:100),
                  Text(
                    'No data found for the chosen date', 
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold,),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height:100),
                ]
              )
            )
          )
        )
      )
    );
  }
  
}

