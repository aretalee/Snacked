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
      title: Text('Were you happy with yesterday\'s eating habits?', style: TextStyle(fontWeight: FontWeight.bold), textAlign: TextAlign.center),
      content: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          const SizedBox(height:30),
          FilledButton(
            onPressed: () {
              widget.viewModel.setPromptFalse();
              context.go('/summary');
            },
            child: const Text('I feel great!'),
          ),
          const SizedBox(height:15),
          FilledButton(
            onPressed: () {
              widget.viewModel.setPromptFalse();
              context.go('/summary');
            },
            child: const Text('Not really...'),
          ),
          const SizedBox(height:15),
          FilledButton(
            onPressed: () {
              widget.viewModel.setPromptFalse();
              context.go('/summary');
            },
            child: const Text('Maybe?'),
          ),
          const SizedBox(height:30),
        ]
      )
    );
  }
}


