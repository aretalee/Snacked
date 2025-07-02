import 'package:firebase_auth/firebase_auth.dart';


class AuthRepository {
  final _auth = FirebaseAuth.instance;

  User? get currentUser => _auth.currentUser;
  Stream<User?> get changes => _auth.authStateChanges();
  String get userID => currentUser!.uid;

  Future<String?> register(String email, String password) async {
    try {
      await _auth.createUserWithEmailAndPassword(
        email: email,
        password: password,
      );
      return 'Success';
    } on FirebaseAuthException catch (e) {
      if (e.code == 'invalid-email') {
        return 'Not a valid email format';
      } else if (e.code == 'email-already-in-use') {
        return 'An account is already associated with this email';
      } else if (e.code == 'weak-password') {
        return('Chosen password is too weak');
      } 
    } catch (e) {
        return e.toString();
      }
    return '';
  }

  Future<String?> login(String email, String password) async {
    try {
      await _auth.signInWithEmailAndPassword(
        email: email,
        password: password,
      );
      return 'Success';
    } on FirebaseAuthException catch (e) {
      if (e.code == 'invalid-email') {
        return 'Not a valid email format';
      } else if (e.code == 'invalid-credential') {
        return 'Invalid email or password';
      } 
    } catch (e) {
        return e.toString();
      }
    return '';
  }

  Future<String?> signOut () async {
    try {
      await _auth.signOut();
      return 'Success';
    } catch (e) {
      return e.toString();
    } 
  }

  Future<String?> resetPassword(String email) async {
    try {
      await _auth.sendPasswordResetEmail(email: email);
      return 'Success';
    } on FirebaseAuthException catch (e) {
      if (e.code == 'invalid-email') {
        return 'Not a valid email format';
      } else if (e.code == 'missing-email') {
        return('Please type in an email to reset password');
      } 
    } catch (e) {
      return e.toString();
    }
    return '';
  }

  Future<String?> changePassword(String oldPwd, String newPwd) async {
    try {
      final credential = EmailAuthProvider.credential(
        email: _auth.currentUser!.email!,
        password: oldPwd,
      );
      await _auth.currentUser?.reauthenticateWithCredential(credential);
      await _auth.currentUser?.updatePassword(newPwd);
      return 'Success';
    } on FirebaseAuthException catch (e) {
      if (e.code == 'requires-recent-login') {
        return 'Please re-login to change password';
      } else if (e.code == 'weak-password') {
        return('Chosen password is too weak');
      } else if (e.code == 'invalid-credential') {
        return 'Invalid email or password provided for authentication';
      } else if (e.code == 'user-mismatch') {
        return 'User details do not match when authenticating';
      } 
    } catch (e) {
      return e.toString();
    }
    return '';
  }

  Future<String?> changeUserame(String name) async {
    try {
      await _auth.currentUser?.updateDisplayName(name);
      return 'Success';
    } catch (e) {
      return e.toString();
    } 
  }

}

