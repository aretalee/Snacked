import 'package:flutter/material.dart';

import 'package:Snacked/ui/export_data/view_model/export_vm.dart';


class ExportPage extends StatefulWidget {
  const ExportPage({super.key, required this.viewModel});
  final ExportViewModel viewModel;

  @override
  State<ExportPage> createState() => _ExportPageState();
}

class _ExportPageState extends State<ExportPage> {

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
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text(
                    'Choose Export Format', 
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold,), 
                    textAlign: TextAlign.center),
                  const SizedBox(height:30),
                  FilledButton(
                      onPressed: () async {
                        if (await widget.viewModel.getJSON()) {
                          await widget.viewModel.exportData();
                          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                              content: Text('Data exported.', style: TextStyle(fontSize: 16, color:Colors.green, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                              duration: const Duration(seconds: 5),
                            )
                          );
                        } else {
                          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                            content: Text('Unable to export data, please try again.', style: TextStyle(fontSize: 16, color:Colors.red, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                            duration: const Duration(seconds: 5),
                            )
                          );
                        }
                      }, 
                      child: const Text('JSON'),
                    ),
                    // const SizedBox(height:15),
                    // FilledButton(
                    //   onPressed: () {}, 
                    //   child: const Text('Excel'),
                    // ),
                ]
              )
            )
          )
        )
      )
    );
  }
  
}


