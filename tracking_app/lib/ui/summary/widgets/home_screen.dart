import 'package:flutter/material.dart';
import 'dart:async';

import 'package:Snacked/global.dart';
import 'package:Snacked/ui/summary/view_model/summary_vm.dart';
import 'package:Snacked/ui/archive/view_model/archive_vm.dart';
import 'package:Snacked/ui/summary/widgets/summary_screen.dart';
import 'package:Snacked/ui/summary/widgets/no_data_screen.dart';

 
 class HomePage extends StatefulWidget {
  const HomePage({super.key, required this.viewModel, required this.viewModelA});
  final SummaryViewModel viewModel;
  final ArchiveViewModel viewModelA;

  @override
  State<HomePage> createState() => _SummaryPageState();
 }

class _SummaryPageState extends State<HomePage> {
  final TextEditingController _commentsController = TextEditingController();
  Timer? _timer;
  late Future<bool> _newData;

  @override
  void initState() {
    super.initState();
    widget.viewModelA.setDate(DateTime.now().subtract(Duration(days:1)));
    _newData = widget.viewModelA.getFromStorage();
    _timer = Timer(widget.viewModel.timerDuration(), () async {
      await fetchService.callFlow();
      await widget.viewModel.addData();
      if (!widget.viewModel.promptShown()) {
        widget.viewModel.updateLastShown();
        widget.viewModel.showPrompt(context, widget.viewModel);
      }

    });
  }

  @override
  void dispose() {
    _commentsController.dispose();
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<bool>(
      future: _newData,
      builder: (BuildContext context, AsyncSnapshot snapshot) {
        if(snapshot.hasData) {
          return SummaryPage(viewModel: widget.viewModel, viewModelA: widget.viewModelA);
        } else if (snapshot.hasError) { return NoDataSummary(); }
        else { return const 
          Center(
            child: Text('Loading')
          );
        }
        
      }
    );
  }
}





