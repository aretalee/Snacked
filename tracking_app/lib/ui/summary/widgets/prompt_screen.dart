import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import 'package:Snacked/ui/summary/view_model/summary_vm.dart';


 class PromptPage extends StatefulWidget {
  const PromptPage({super.key, required this.viewModel});
  final SummaryViewModel viewModel;

  @override
  State<PromptPage> createState() => _PromptPageState();
 }

class _PromptPageState extends State<PromptPage> {

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Text('Do you think you snacked more or less than yesterday?', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
      content: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          const SizedBox(height:5),
          Text('Choose an option below to see!', style: TextStyle(fontSize: 16), textAlign: TextAlign.center),
          const SizedBox(height:30),
          FilledButton(
            onPressed: () {
              widget.viewModel.setPromptFalse();
              context.go('/summary');
            },
            child: const Text('Less :)'),
          ),
          const SizedBox(height:15),
          FilledButton(
            onPressed: () {
              widget.viewModel.setPromptFalse();
              context.go('/summary');
            },
            child: const Text('More :('),
          ),
          const SizedBox(height:15),
          FilledButton(
            onPressed: () {
              widget.viewModel.setPromptFalse();
              context.go('/summary');
            },
            child: const Text('Not sure'),
          ),
          const SizedBox(height:30),
        ]
      )
    );
  }
}


